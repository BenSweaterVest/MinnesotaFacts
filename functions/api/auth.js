// functions/api/auth.js

// Handle all HTTP methods through a single export
export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);
        
        // Add CORS headers to all responses
        const corsHeaders = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        };
        
        // Handle CORS preflight
        if (request.method === 'OPTIONS') {
            return new Response(null, {
                status: 200,
                headers: corsHeaders
            });
        }
        
        // Only allow POST requests for authentication
        if (request.method !== 'POST') {
            return new Response(JSON.stringify({
                success: false,
                message: 'Method not allowed. Use POST.'
            }), {
                status: 405,
                headers: {
                    'Content-Type': 'application/json',
                    ...corsHeaders
                }
            });
        }
        
        try {
            const body = await request.json();
            const { password } = body;
            
            // Debug logging
            console.log('Function called with password:', password);
            console.log('Expected password:', env.Page_Password);
            console.log('GitHub token available:', !!env.Github_Token);
            
            // Check if password matches
            if (password === env.Page_Password) {
                return new Response(JSON.stringify({
                    success: true,
                    githubToken: env.Github_Token,
                    message: 'Authentication successful'
                }), {
                    status: 200,
                    headers: {
                        'Content-Type': 'application/json',
                        ...corsHeaders
                    }
                });
            } else {
                return new Response(JSON.stringify({
                    success: false,
                    message: 'Invalid password'
                }), {
                    status: 401,
                    headers: {
                        'Content-Type': 'application/json',
                        ...corsHeaders
                    }
                });
            }
        } catch (error) {
            console.error('Authentication error:', error);
            return new Response(JSON.stringify({
                success: false,
                message: 'Server error: ' + error.message
            }), {
                status: 500,
                headers: {
                    'Content-Type': 'application/json',
                    ...corsHeaders
                }
            });
        }
    }
};

// Alternative export format for Cloudflare Pages
export async function onRequest(context) {
    const { request, env } = context;
    
    // Add CORS headers to all responses
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    };
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
        return new Response(null, {
            status: 200,
            headers: corsHeaders
        });
    }
    
    // Only allow POST requests for authentication
    if (request.method !== 'POST') {
        return new Response(JSON.stringify({
            success: false,
            message: 'Method not allowed. Use POST.'
        }), {
            status: 405,
            headers: {
                'Content-Type': 'application/json',
                ...corsHeaders
            }
        });
    }
    
    try {
        const body = await request.json();
        const { password } = body;
        
        // Debug logging
        console.log('Function called with password:', password);
        console.log('Expected password:', env.Page_Password);
        console.log('GitHub token available:', !!env.Github_Token);
        
        // Check if password matches
        if (password === env.Page_Password) {
            return new Response(JSON.stringify({
                success: true,
                githubToken: env.Github_Token,
                message: 'Authentication successful'
            }), {
                status: 200,
                headers: {
                    'Content-Type': 'application/json',
                    ...corsHeaders
                }
            });
        } else {
            return new Response(JSON.stringify({
                success: false,
                message: 'Invalid password'
            }), {
                status: 401,
                headers: {
                    'Content-Type': 'application/json',
                    ...corsHeaders
                }
            });
        }
    } catch (error) {
        console.error('Authentication error:', error);
        return new Response(JSON.stringify({
            success: false,
            message: 'Server error: ' + error.message
        }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
                ...corsHeaders
            }
        });
    }
}
