// functions/api/auth.js

export async function onRequest(context) {
    const { request, env } = context;
    
    // Add CORS headers to all responses
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    };
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
        return new Response(null, {
            status: 200,
            headers: corsHeaders
        });
    }
    
    // Handle GET request (for testing)
    if (request.method === 'GET') {
        return new Response(JSON.stringify({
            success: false,
            message: 'This endpoint requires POST method',
            method: request.method,
            url: request.url
        }), {
            status: 405,
            headers: corsHeaders
        });
    }
    
    // Only allow POST requests for authentication
    if (request.method !== 'POST') {
        return new Response(JSON.stringify({
            success: false,
            message: `Method ${request.method} not allowed. Use POST.`,
            allowedMethods: ['POST', 'OPTIONS']
        }), {
            status: 405,
            headers: corsHeaders
        });
    }
    
    try {
        // Parse request body
        const body = await request.json();
        const { password } = body;
        
        // Debug logging
        console.log('Authentication attempt');
        console.log('Received password:', password);
        console.log('Expected password:', env.Page_Password);
        console.log('Environment variables available:', Object.keys(env));
        console.log('GitHub token available:', !!env.Github_Token);
        
        // Validate input
        if (!password) {
            return new Response(JSON.stringify({
                success: false,
                message: 'Password is required'
            }), {
                status: 400,
                headers: corsHeaders
            });
        }
        
        // Check environment variables
        if (!env.Page_Password) {
            console.error('Page_Password environment variable not set');
            return new Response(JSON.stringify({
                success: false,
                message: 'Server configuration error'
            }), {
                status: 500,
                headers: corsHeaders
            });
        }
        
        // Check if password matches
        if (password === env.Page_Password) {
            console.log('Password match successful');
            return new Response(JSON.stringify({
                success: true,
                githubToken: env.Github_Token || null,
                message: 'Authentication successful'
            }), {
                status: 200,
                headers: corsHeaders
            });
        } else {
            console.log('Password mismatch');
            return new Response(JSON.stringify({
                success: false,
                message: 'Invalid password'
            }), {
                status: 401,
                headers: corsHeaders
            });
        }
    } catch (error) {
        console.error('Authentication error:', error);
        return new Response(JSON.stringify({
            success: false,
            message: 'Server error: ' + error.message,
            error: error.name
        }), {
            status: 500,
            headers: corsHeaders
        });
    }
}
