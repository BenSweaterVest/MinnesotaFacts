/*\
title: $:/plugins/collaborative-blog/test-action.js
type: application/javascript
module-type: widget

Action widget to test Cloudflare save connection

\*/
(function(){

  'use strict';

  const Widget = require('$:/core/modules/widgets/widget.js').widget;

  const TestCloudflareAction = function(parseTreeNode,options) {
    this.initialise(parseTreeNode,options);
  };

  TestCloudflareAction.prototype = new Widget();

  TestCloudflareAction.prototype.render = function(_parent,_nextSibling) {
    this.computeAttributes();
    this.execute();
  };

  TestCloudflareAction.prototype.execute = function() {
    // Nothing to execute
  };

  TestCloudflareAction.prototype.refresh = function(_changedTiddlers) {
    return false;
  };

  TestCloudflareAction.prototype.invokeAction = function(_triggeringWidget,_event) {
    const self = this;

    // Get configuration
    const endpoint = $tw.wiki.getTiddlerText('$:/config/cloudflare-saver/endpoint', '');
    const enabled = $tw.wiki.getTiddlerText('$:/config/cloudflare-saver/enabled', 'no') === 'yes';

    // Validate configuration
    if (!enabled) {
      self.showAlert('Cloudflare Saver is not enabled. Please enable it in the settings above.', 'error');
      return true;
    }

    if (!endpoint || endpoint.trim() === '') {
      self.showAlert('No Cloudflare Function endpoint configured. Please enter your endpoint URL above.', 'error');
      return true;
    }

    // Get password
    const password = prompt('Enter your Cloudflare save password to test the connection:');
    if (!password) {
      self.showAlert('Test cancelled - no password provided.', 'info');
      return true;
    }

    // Show loading state
    self.showNotification('$:/plugins/collaborative-blog/notifications/saving');

    // Create test content
    const testContent = $tw.wiki.renderTiddler('text/plain', '$:/core/save/all');

    // Attempt to save
    const timeout = Math.max(5, parseInt($tw.wiki.getTiddlerText('$:/config/cloudflare-saver/timeout', '30')) || 30) * 1000;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    const payload = {
      content: testContent,
      password,
      timestamp: new Date().toISOString(),
      retryCount: 0
    };

    fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload),
      signal: controller.signal
    })
      .then((response) => {
        clearTimeout(timeoutId);

        if (response.ok) {
          return response.json().then((data) => {
            self.showNotification('$:/plugins/collaborative-blog/notifications/success');
            self.showAlert(
              `Test successful\n\nConnection to Cloudflare Function verified.\nCommit SHA: ${data.commit || 'N/A'}\n\nYour Cloudflare Saver is configured correctly.`,
              'success'
            );
          });
        } else {
          return response.text().then((errorText) => {
            let errorMsg = `HTTP ${response.status} ${response.statusText}`;
            try {
              const errorData = JSON.parse(errorText);
              if (errorData.error) {
                errorMsg = errorData.error;
              }
            } catch (e) {
              // Use status text
            }

            self.showNotification('$:/plugins/collaborative-blog/notifications/failure');
            self.showAlert(
              `Test failed\n\nError: ${errorMsg}\n\nPlease check:\n• Endpoint URL is correct\n• Password matches SAVE_PASSWORD in Cloudflare\n• Environment variables are configured\n• Cloudflare Function is deployed`,
              'error'
            );
          });
        }
      })
      .catch((error) => {
        clearTimeout(timeoutId);

        let errorMsg = 'Network error';
        if (error.name === 'AbortError') {
          errorMsg = 'Request timeout';
        } else {
          errorMsg = error.message;
        }

        self.showNotification('$:/plugins/collaborative-blog/notifications/failure');
        self.showAlert(
          `Test failed\n\nError: ${errorMsg}\n\nPlease check:\n• Internet connection\n• Endpoint URL is accessible\n• CORS is configured to allow your origin\n• Cloudflare Function is deployed`,
          'error'
        );
      });

    return true; // Prevent default action
  };

  TestCloudflareAction.prototype.showAlert = function(message, type) {
    const tempTiddler = '$:/temp/cloudflare-test-result';

    let title = 'Cloudflare Save Test';
    let color = '';

    if (type === 'success') {
      title = 'Test Successful';
      color = 'green';
    } else if (type === 'error') {
      title = 'Test Failed';
      color = 'red';
    } else if (type === 'info') {
      title = 'Test Cancelled';
      color = 'blue';
    }

    const formattedText = `<div style="background-color: ${color === 'green' ? '#d4edda' : color === 'red' ? '#f8d7da' : '#d1ecf1'}; border: 1px solid ${color === 'green' ? '#c3e6cb' : color === 'red' ? '#f5c6cb' : '#bee5eb'}; border-radius: 4px; padding: 15px; margin: 10px 0;">

!! ${title}

${message.split('\n').map(line => line.trim()).filter(line => line).join('\n\n')}

</div>`;

    $tw.wiki.addTiddler(new $tw.Tiddler({
      title: tempTiddler,
      text: formattedText,
      type: 'text/vnd.tiddlywiki',
      'modal-title': title
    }));

    $tw.modal.display(tempTiddler, {
      downloadLink: null
    });
  };

  TestCloudflareAction.prototype.showNotification = function(tiddlerTitle) {
    if (typeof $tw !== 'undefined' && $tw.notifier) {
      $tw.notifier.display(tiddlerTitle);
    }
  };

  exports['action-test-cloudflare'] = TestCloudflareAction;

})();
