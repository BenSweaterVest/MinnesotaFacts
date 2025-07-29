export async function onRequest(context) {
    const { request, env } = context;
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
        return new Response(null, {
            status: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
        });
    }
    
    // Only allow POST requests
    if (request.method !== 'POST') {
        return new Response(JSON.stringify({
            success: false,
            message: 'Method not allowed'
        }), {
            status: 405,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        });
    }
    
    try {
        const { password } = await request.json();
        
        // Debug logging (remove in production)
        console.log('Received password:', password);
        console.log('Expected password:', env.Page_Password);
        console.log('GitHub token exists:', !!env.Github_Token);
        
        // Check if password matches the Page_Password secret
        if (password === env.Page_Password) {
            // Password is correct, return the GitHub token from secrets
            return new Response(JSON.stringify({
                success: true,
                githubToken: env.Github_Token,
                message: 'Authentication successful'
            }), {
                status: 200,
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            });
        } else {
            // Password is incorrect
            return new Response(JSON.stringify({
                success: false,
                message: 'Invalid password'
            }), {
                status: 401,
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            });
        }
    } catch (error) {
        console.error('Authentication error:', error);
        return new Response(JSON.stringify({
            success: false,
            message: 'Server error'
        }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        });
    }
}
