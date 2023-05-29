# NL3 Cognito Pre-Authentication Lambda Function for Performing Account Protection Check
This integration allows Amazon Cognito customers to integrate a pre-authentication Lambda function to check the lock status for their users' accounts and block access if locked. This integration requires an active license with Next Level3. Please visit www.nextlevel3.com for more details on how to sign up for NL3 Account Protection.

## Steps for creating Lambda layer
1. Log into AWS with permissions to create Lambda functions, Lambda layers, and modify Cognito User Pools
2. In the Search box at the top, type "Lambda" and open the "Lambda" service
3. Select "Layers" in the left-hand menu
4. Select "Create layer"
5. Enter a "Name" for the function (e.g., nl3-python-layer)
6. Select "Upload a .zip file"
7. Click "Upload" and browser to the "./nl3-python-layer/aws-layer/lambda-layer.zip" file from this repository or one you created on your own with the required dependencies from the requirements.txt file
8. Select the x86_64 checkbox from the list of "Compatible architectures"
9. Select the "Compatible runtimes" from the drop-down list (e.g., Python 3.8 and Python 3.9 for the included lambda-layer.zip)
10. Select "Create"

## Steps for creating Lambda function
1. Log into AWS with permissions to create Lambda functions, Lambda layers, and modify Cognito User Pools
2. In the Search box at the top, type "Lambda" and open the "Lambda" service
3. Select the "Create Function" button in the upper right-hand corner
4. Leave the "Author from scratch" radio button selected and enter a function name (e.g., nl3CognitoProtectionCheckPython)
5. In the "Runtime" drop-down box, select "Python 3.9"
6. Under "Architecture" leave the "x86_64" radio button selected
7. Click "Create function"
8. Copy and Paste the code from the "nl3CognitoProtectionCheckPython/lambda_function.py" in this repository into the lambda_function.py file in the "Code source" editor (replace any current, default code completely)
9. Select "File > Save" in the "Code source" editor
10. Scroll up to the "Function overview" section and select "Layers"
11. In the "Layers" section, select "Add a layer"
12. Click "Custom layers" from the radio buttons
13. In the "Custom layers" drop-down choose "nl3-python-layer", then under the "Version" drop-down "1"
14. Click "Add"
15. Select the "Configuration" tab below the "Function overview" section and then select "Environment variables" and create and set the following variables:

| Secret Name | Secret Value (description of value) |
| ----------- | ----------------------------------- |
| SIGNING_KEY | The base64 encoded signing key associated with the application you are integrating with from the NL3 company portal (company.nextlevel3.com) |
| APP_FQDN | The fully-qualified domain name associated with your application and SIGNING_KEY |
| CLIENT_ID | The Cognito User Pool Client ID associated with the application you wish to add an NL3 Account Protection Check (This value can be found on the "App Integration" tab in the Cognito User Pool settings in the App client list > App clients and analytics section) |
| API_URI | The URI for the NL3 external API (e.g., https://api.nextlevel3.com - see NL3 product documentation or contact your account representative) |
| API_PATH | The path to the account protection check API method (e.g.,  /nl3/api/v1/accountProtectionCheck) |
| LOCKED_MESSAGE | The message to display to the end user if the account is locked (e.g. "Either the username and/or password are incorrect or the user account is locked") |

16. Return to the "Code" tab and click "Deploy"
17. NOTE: If you have customized the Lambda function to add logic and are getting timeouts, consider adjusting the "Timeout" value under "Configuration > General configuration" (default is 3 seconds)

## Integrate Lambda Function into Cognito User Pool Authentication Flow
1. Log into AWS with permissions to create Lambda functions, Lambda layers, and modify Cognito User Pools
2. In the search box at the top, type "Cognito" and click on the "Cognito" service
3. Under "User pools" click on the appropriate "User pool name"
4. Select the "User pool properties" tab and click "Add Lambda trigger"
5. Select the "Authentication" radio button, then choose the "Pre authentication trigger" radio button that displays below
6. Select the Lambda function you created (e.g., nl3CognitoProtectionCheckPython) from the "Assign lambda function" drop-down
7. Click "Add Lambda trigger"


## Test Integration
First, enable a user account for this application. Then, attempt to authenticate with the user account locked and then again with the user account unlocked.

## Integration Complete

# NL3 Auth0 Action for Performing Account Protection Check Plus Enable Users
This integration allows auth0 customers to integrate a post login action to check the lock status for their users' accounts and block access if locked. This integration will aslo create a user in NL3 and enable the auth0 account for locking. NOTE 1: if you use this action DO NOT use the integration above. NOTE 2: this will create a new NL3 user with the same email as the user for the application you add it to. It currently does not support an existing NL3 account, but that could be easily added (please contact support for more info). This integration requires an active license with Next Level3. Please visit www.nextlevel3.com for more details on how to sign up for NL3 Account Protection.

## Steps for configuring as a custom action
1. Log into manage.auth0.com as a user with permissions to create and modify custom actions
2. In the left-side menu select Actions > Library
3. Select the "Build Custom" button in the upper right-hand corner
4. Give the action a descriptive name in the "Name" field (e.g. NL3 Account Protection Check and User Enablement)
5. Select "Login / Post Login" for "Trigger"
6. Select "Node 16 (Recommended)" for "Runtime"
7. Click "Create"
8. Copy and Paste the code from the "NL3-Account-Protection-Check-Plus-Enable-User.js" in this repository into the action (replace any current, default code completely)
9. Select the icon that looks like a package called "Modules"
10. Select "Add Module"
11. In the "Name" textbox type njwt
12. Click "Create"
13. Select the icon that looks like a skeleton key called "Secrets"
14. Add the following secrets:

| Secret Name | Secret Value (description of value) |
| ----------- | ----------------------------------- |
| SIGNING_KEY | The base64 encoded signing key associated with the application you are integrating with from the NL3 company portal (company.nextlevel3.com) |
| APP_URI | The fully-qualified domain name associated with your application and SIGNING_KEY |
| CLIENT_ID | The Auth0 Client ID associated with the application you wish to add an NL3 Account Protection Check (This value can be found at manage.auth0.com by selecting Applications > Applications on the left-side menu. It will be in the right-hand column of the list of applications. |
| API_HOST | The domain name for the NL3 external API (e.g., api.nextlevel3.com - see NL3 product documentation or contact your account representative) |
| API_PATH | The path to the account protection check API method (e.g.,  /nl3/api/v1/accountProtectionCheck) |
| EU_API_PATH | The path to the account protection check API method (e.g.,  /nl3/api/v1/sdk/importUsers) |
| SDK_API_KEY | Retrieve SDK API key from company portal under Keys & Tokens in the side menu |
| LOCKED_MESSAGE | The message to display to the end user if the account is locked (e.g. "Either the username and/or password are incorrect or the user account is locked") |
| FAIL_OPEN | Set to 'true' without quotes if you want the lock check to fail open, otherwise set it to 'false' without quotes. |

## Integrate into Actions "Login" Flow
1. Log into manage.auth0.com as a user with permissions to create and modify action flows
2. In the left-side menu select "Actions > Flows"
3. Select "Login" from the tiles under the "Flows" header
4. In the side panel with the "Add Action" header, select the "Custom" tab
5. Find the Custom Action you created above and drag it into one of the "Drop Here" boxes that display below the "Start > User Logged In" and "Complete - Token Issued" flow designators when you start to drag over the custom action and make sure when you release it the action remains in the flow
6. Select "Apply" in the top right to add the action to the flow


## Test Integration
First, enable a user account for this application. Then, attempt to authenticate with the user account locked and then again with the user account unlocked.

## Integration Complete
