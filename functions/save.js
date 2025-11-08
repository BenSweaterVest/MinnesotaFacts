// Cloudflare Pages Function for TiddlyWiki saving
// Based on tiddlywiki-cloudflare-saver demo/functions/save.js

const ALLOWED_ORIGINS = '*'; // Allow all origins for local file:// access
const MAX_CONTENT_SIZE = 52428800; // 50MB
const RATE_LIMIT_WINDOW = 60000; // 1 minute
const RATE_LIMIT_MAX = 30; // requests per window

// In-memory rate limiting (resets on function cold start)
const rateLimitMap = new Map();

function checkRateLimit(ip) {
  const now = Date.now();
  const record = rateLimitMap.get(ip) || { count: 0, windowStart: now };

  if (now - record.windowStart > RATE_LIMIT_WINDOW) {
    record.count = 1;
    record.windowStart = now;
  } else {
    record.count++;
  }

  rateLimitMap.set(ip, record);
  return record.count <= RATE_LIMIT_MAX;
}

function getCorsHeaders(origin) {
  const allowedOrigin = origin === 'null' || !origin ? '*' : origin;
  return {
    'Access-Control-Allow-Origin': allowedOrigin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Password',
    'Access-Control-Max-Age': '86400',
  };
}

export async function onRequestOptions(context) {
  try {
    const origin = context.request.headers.get('Origin');
    return new Response(null, {
      status: 200,
      headers: getCorsHeaders(origin),
    });
  } catch (error) {
    // Always return valid CORS response even on error
    return new Response(null, {
      status: 200,
      headers: getCorsHeaders('*'),
    });
  }
}

export async function onRequestPost(context) {
  const { request, env } = context;
  const origin = request.headers.get('Origin');
  const corsHeaders = getCorsHeaders(origin);

  try {
    // Rate limiting
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    if (!checkRateLimit(ip)) {
      return new Response(JSON.stringify({ error: 'Rate limit exceeded' }), {
        status: 429,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Authentication
    const password = request.headers.get('X-Password');
    if (!password || password !== env.SAVE_PASSWORD) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Get wiki content
    const contentType = request.headers.get('Content-Type') || '';
    let wikiContent;

    if (contentType.includes('application/json')) {
      const json = await request.json();
      wikiContent = json.content || json.wiki;
    } else {
      wikiContent = await request.text();
    }

    if (!wikiContent) {
      return new Response(JSON.stringify({ error: 'No content provided' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Check size
    const contentSize = new TextEncoder().encode(wikiContent).length;
    if (contentSize > (env.MAX_CONTENT_SIZE || MAX_CONTENT_SIZE)) {
      return new Response(JSON.stringify({ error: 'Content too large' }), {
        status: 413,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Prepare GitHub API request
    const GITHUB_REPO = env.GITHUB_REPO || 'BenSweaterVest/MinnesotaFacts';
    const FILE_PATH = env.FILE_PATH || 'index.html';
    const BRANCH = env.GITHUB_BRANCH || 'main';
    const [owner, repo] = GITHUB_REPO.split('/');

    // Encode content in chunks to avoid memory issues with large files
    const encoder = new TextEncoder();
    const bytes = encoder.encode(wikiContent);
    const CHUNK_SIZE = 65536; // 64KB chunks
    let base64 = '';

    for (let i = 0; i < bytes.length; i += CHUNK_SIZE) {
      const chunk = bytes.slice(i, Math.min(i + CHUNK_SIZE, bytes.length));
      const chunkArray = Array.from(chunk);
      const chunkString = String.fromCharCode(...chunkArray);
      base64 += btoa(chunkString);
    }

    // Get current file SHA with retry logic
    let sha = null;
    let retryCount = 0;
    const MAX_RETRIES = 3;

    while (retryCount < MAX_RETRIES) {
      try {
        const getResponse = await fetch(
          `https://api.github.com/repos/${owner}/${repo}/contents/${FILE_PATH}?ref=${BRANCH}`,
          {
            headers: {
              'Authorization': `token ${env.GITHUB_TOKEN}`,
              'Accept': 'application/vnd.github.v3+json',
              'User-Agent': 'TiddlyWiki-Cloudflare-Saver',
            },
          }
        );

        if (getResponse.ok) {
          const data = await getResponse.json();
          sha = data.sha;
          break;
        } else if (getResponse.status === 404) {
          // File doesn't exist yet
          break;
        }
      } catch (error) {
        retryCount++;
        if (retryCount >= MAX_RETRIES) throw error;
        await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
      }
    }

    // Commit to GitHub
    const commitMessage = `Update wiki - ${new Date().toISOString()}`;
    const updateData = {
      message: commitMessage,
      content: base64,
      branch: BRANCH,
    };

    if (sha) {
      updateData.sha = sha;
    }

    retryCount = 0;
    while (retryCount < MAX_RETRIES) {
      try {
        const putResponse = await fetch(
          `https://api.github.com/repos/${owner}/${repo}/contents/${FILE_PATH}`,
          {
            method: 'PUT',
            headers: {
              'Authorization': `token ${env.GITHUB_TOKEN}`,
              'Accept': 'application/vnd.github.v3+json',
              'Content-Type': 'application/json',
              'User-Agent': 'TiddlyWiki-Cloudflare-Saver',
            },
            body: JSON.stringify(updateData),
          }
        );

        if (putResponse.ok) {
          const result = await putResponse.json();
          return new Response(JSON.stringify({
            success: true,
            message: 'Wiki saved successfully',
            commit: result.commit.sha,
          }), {
            status: 200,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        } else if (putResponse.status === 409) {
          // Conflict - retry with new SHA
          retryCount++;
          if (retryCount >= MAX_RETRIES) {
            return new Response(JSON.stringify({ error: 'Conflict - please retry' }), {
              status: 409,
              headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            });
          }
          await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
          continue;
        } else {
          const errorText = await putResponse.text();
          return new Response(JSON.stringify({
            error: 'GitHub API error',
            details: errorText,
          }), {
            status: putResponse.status,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        }
      } catch (error) {
        retryCount++;
        if (retryCount >= MAX_RETRIES) {
          throw error;
        }
        await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
      }
    }

  } catch (error) {
    console.error('Save error:', error);
    return new Response(JSON.stringify({
      error: 'Server error',
      message: error.message,
    }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
}
