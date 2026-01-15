/*\
title: $:/plugins/collaborative-blog/saver.js
type: application/javascript
module-type: saver

Cloudflare Functions saver module for TiddlyWiki.

Provides server-side GitHub integration via Cloudflare Functions.
Implements password authentication, retry logic, and error handling.

\*/
(function(){

  'use strict';

  /**
   * CloudflareSaver constructor
   * @param {Object} wiki - TiddlyWiki wiki object
   */
  const CloudflareSaver = function(wiki) {
    this.wiki = wiki;
    this.sessionPassword = null;

    // Register event listener for password clearing
    const self = this;
    $tw.rootWidget.addEventListener('cloudflare-clear-password', () => {
      self.sessionPassword = null;
    });
  };

  CloudflareSaver.prototype.save = function(text, method, callback, options) {
    const self = this;
    options = options || {};

    // Verify saver is enabled in configuration
    const enabled = self.wiki.getTiddlerText('$:/config/cloudflare-saver/enabled', 'no') === 'yes';
    if (!enabled) {
      return false;
    }

    // Verify endpoint is configured
    const endpoint = self.wiki.getTiddlerText('$:/config/cloudflare-saver/endpoint', '');
    if (!endpoint || endpoint.trim() === '') {
      return false;
    }

    // Only handle save and autosave methods
    if (method !== 'save' && method !== 'autosave') {
      return false;
    }

    // Load configuration from tiddlers
    const config = {
      endpoint,
      timeout: Math.max(5, parseInt(self.wiki.getTiddlerText('$:/config/cloudflare-saver/timeout', '30')) || 30) * 1000,
      notifications: self.wiki.getTiddlerText('$:/config/cloudflare-saver/notifications', 'yes') === 'yes',
      autoRetry: self.wiki.getTiddlerText('$:/config/cloudflare-saver/auto-retry', 'yes') === 'yes',
      rememberPassword: self.wiki.getTiddlerText('$:/config/cloudflare-saver/remember-password', 'no') === 'yes',
      debug: self.wiki.getTiddlerText('$:/config/cloudflare-saver/debug', 'no') === 'yes'
    };

    if (config.debug) {
      console.log('[CloudflareSaver] Save initiated');
    }

    // Retrieve password from session or prompt user
    let password = null;
    if (config.rememberPassword && self.sessionPassword) {
      password = self.sessionPassword;
    } else {
      password = prompt('Enter Cloudflare save password:');
      if (!password) {
        callback('Save cancelled by user');
        return false;
      }
      if (config.rememberPassword) {
        self.sessionPassword = password;
      }
    }

    // Display saving notification
    if (config.notifications && typeof $tw !== 'undefined' && $tw.notifier) {
      $tw.notifier.display('$:/plugins/collaborative-blog/notifications/saving');
    }

    self._performSave(text, password, callback, config, 0);
    return true;
  };

  CloudflareSaver.prototype._performSave = async function(text, password, callback, config, retryCount) {
    const self = this;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), config.timeout);

    try {
      const payload = {
        content: text,
        password,
        timestamp: new Date().toISOString(),
        retryCount
      };

      const response = await fetch(config.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (response.ok) {
        if (config.debug) {
          console.log('[CloudflareSaver] Save completed successfully');
        }

        self._incrementStat('successful-saves');
        self._updateLastSave('success');

        callback(null);
        if (config.notifications && typeof $tw !== 'undefined' && $tw.notifier) {
          $tw.notifier.display('$:/plugins/collaborative-blog/notifications/success');
        }
      } else {
        const responseText = await response.text();
        self._handleSaveError(response.status, response.statusText, responseText, password, text, callback, config, retryCount);
      }
    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === 'AbortError') {
        self._handleSaveError(0, 'Request timeout', '', password, text, callback, config, retryCount);
      } else {
        self._handleSaveError(0, 'Network error', error.message, password, text, callback, config, retryCount);
      }
    }
  };

  CloudflareSaver.prototype._handleSaveError = function(status, statusText, responseText, password, text, callback, config, retryCount) {
    const self = this;
    const maxRetries = config.autoRetry ? 3 : 0;

    let errorMsg = 'Save failed';
    if (status) {
      errorMsg += `: HTTP ${status}`;
      if (statusText) {
        errorMsg += ` ${statusText}`;
      }
    }

    // Parse JSON error response if available
    if (responseText) {
      try {
        const response = JSON.parse(responseText);
        if (response.error) {
          errorMsg += ` - ${response.error}`;
        }
        if (response.resetIn) {
          errorMsg += ` (retry in ${response.resetIn} seconds)`;
        }
      } catch (e) {
        if (responseText.length < 200) {
          errorMsg += ` - ${responseText}`;
        }
      }
    }

    // Handle specific HTTP status codes
    if (status === 401) {
      self.sessionPassword = null;
      errorMsg = 'Authentication failed. Check your password.';
    } else if (status === 429) {
      errorMsg = 'Rate limit exceeded. Wait before retrying.';
    } else if (status === 413) {
      errorMsg = 'Content too large. TiddlyWiki exceeds maximum size.';
    } else if (status === 409) {
      errorMsg = 'Conflict detected. Another save may be in progress.';
    }

    if (config.debug) {
      console.error('[CloudflareSaver] Error:', errorMsg, {
        status,
        retryCount,
        willRetry: retryCount < maxRetries && status !== 401
      });
    }

    // Implement retry with exponential backoff (skip auth failures and rate limits)
    if (retryCount < maxRetries && status !== 401 && status !== 429) {
      const retryDelay = Math.min(1000 * Math.pow(2, retryCount), 10000);
      if (config.debug) {
        console.log(`[CloudflareSaver] Retrying in ${retryDelay / 1000} seconds`);
      }
      setTimeout(() => {
        self._performSave(text, password, callback, config, retryCount + 1);
      }, retryDelay);
    } else {
      self._incrementStat('failed-saves');
      self._updateLastSave('failure', errorMsg);

      callback(errorMsg);
      if (config.notifications && typeof $tw !== 'undefined' && $tw.notifier) {
        $tw.notifier.display('$:/plugins/collaborative-blog/notifications/failure');
      }
    }
  };

  CloudflareSaver.prototype._incrementStat = function(statName) {
    const tiddlerTitle = `$:/config/cloudflare-saver/stats/${statName}`;
    const currentValue = parseInt(this.wiki.getTiddlerText(tiddlerTitle, '0')) || 0;
    this.wiki.addTiddler(new $tw.Tiddler({
      title: tiddlerTitle,
      text: String(currentValue + 1)
    }));
  };

  CloudflareSaver.prototype._updateLastSave = function(status, error) {
    const timestamp = new Date().toISOString();
    this.wiki.addTiddler(new $tw.Tiddler({
      title: '$:/config/cloudflare-saver/stats/last-save-status',
      text: status,
      'last-save-time': timestamp,
      'last-save-error': error || ''
    }));
  };

  CloudflareSaver.prototype.info = {
    name: 'cloudflare',
    priority: 2000,
    capabilities: ['save', 'autosave']
  };

  exports.info = {
    name: 'cloudflare',
    priority: 2000,
    capabilities: ['save', 'autosave']
  };

  exports.canSave = function(wiki) {
    const enabled = $tw.wiki.getTiddlerText('$:/config/cloudflare-saver/enabled', 'no') === 'yes';
    const endpoint = $tw.wiki.getTiddlerText('$:/config/cloudflare-saver/endpoint', '');
    return enabled && endpoint && endpoint.trim() !== '';
  };

  exports.create = function(wiki) {
    return new CloudflareSaver(wiki);
  };

})();
