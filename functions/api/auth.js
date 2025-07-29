export async function onRequestPost(context) {
    const { request, env } = context;
    
    try {
        const { password } = await request.json();
        
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

// Handle OPTIONS request for CORS
export async function onRequestOptions(context) {
    return new Response(null, {
        status: 200,
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }
    });
}
