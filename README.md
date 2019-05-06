# Orchestrator_bot
Orchestrator Bot deployed in dialogflow
## Dialogflow Webhook Orchestrator bot implementation in Python
This service takes `Process Id` and 'Process Name' as params from Dialogflow JSON request and login to the orchestrator, runs specific job and return a webhook response

More info about Dialogflow webhooks could be found here:
[Dialogflow Webhook](https://dialogflow.com/docs/fulfillment)

# Deploy to Heroku:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# How to use?
* Create a new agent in [Dialogflow](https://dialogflow.com/)
* Provide your fulfillment info. Deploy using heroku or provide your own. (https//www.example.com/webhook)
* Provide API key of OWM as OWMApiKey with value in Config Vars of heroku (or) use your key directly in the file. 
* Create the intent (like weather in singapore [$geo-city] ) and enable webhook fulfillment in the intent
* Test in your console
# Examples
#### start job with id {} and name {}
Response Status:   
 

### Terms
* [Google APIs Terms](https://developers.google.com/terms/).
