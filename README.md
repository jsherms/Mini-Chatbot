# Mini-Chatbot
Prerequisites:
  Please ensure you have the following installed on your machine:
  - [Python](https://www.python.org/downloads/)
  - [pip](https://pip.pypa.io/en/stable/installation/)
  - [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

Follow these instructions to get the chatbot Restful API working on your local machine
## 1. Clone repository ##
Please navigate to the directory where you would like to clone the repository and execute these commands in the terminal

     git clone https://github.com/jsherms/Mini-Chatbot.git
     cd Mini-Chatbot
   
Great! You have now successfully cloned the repository. Now lets get our API up and running.
  
     
## 2. Running the server

First, we must move into our project directory folder. Within the Mini-Chatbot folder, please navigate to the chatbot folder

    cd chatbot

Once you are in the chatbot folder, you are ready to activate the server

To activate the server, execute the following command:

    python3 manage.py runserver

To ensure the server is running as expected, navigate to (http://127.0.0.1:8000/). You should see this page:
<img width="1260" alt="Chatbot Home Page" src="https://github.com/user-attachments/assets/5e18c367-cdde-4995-b39d-a4d43af0b1c6">

If you see this page, you are set to use the API!.

## 3. Using the endpoints

As you can see in the home page, we have 4 endpoints that can be hit. The first one we will walk through is register_user

### Register New User
Click on the URL you see in the list of API endpoints for register_user or click [here](127.0.0.1:8000/register_user/) if your server is running
<img width="1260" alt="Register User Page" src="https://github.com/user-attachments/assets/38fa9d5b-c665-4fbc-a298-ce95bd633a9c">

Here input your name and email into the HTML form and select POST. You can also use the raw form, with the payload of 
    
    {
      "name": "",
      "email": ""
    }

NOTE: Name and email must both be no greater than 40 characters
If you submit a valid payload, the response should look like 
    
    {
      "id": 4,
      "name": "Name",
      "email": "Email@Email.com"
    }
**MAKE SURE YOU REMEMBER YOUR USER ID YOU WILL NEED IT LATER**
Once you have succesfully registered the user, you can return to the home page!

### Get FAQs
Before we begin our conversation, lets see what FAQs exist. Navigate to the Get_FAQ URL from the homepage or click [here](http://127.0.0.1:8000/get_faqs/)

On the page load, all the existing FAQs will appear. If you wish to filter based on a certain category, navigate to the filters tab in the top right and input what category you wish to search for
<img width="1260" alt="Filter FAQs" src="https://github.com/user-attachments/assets/94386db8-6aa9-4f0a-91d0-fc1686241c00">

If you wish to see all FAQs again, just delete what is in the category filter and post again.

### Start a conversation
Now that we know what questions are available and contain answers, lets start a new conversation.

Navigate to the home page once more and select the create_conversation [URL](http://127.0.0.1:8000/create_conversation/)
Here you will send the endpoint your user id which you grabbed from the register user endpoint.
<img width="1260" alt="Create Conversation Endpoint" src="https://github.com/user-attachments/assets/3f7a7029-3015-4282-b21d-0ef56d6d6220">

You can select your user ID from the HTML form or use the raw data and pass a json of 

    {
      "user": int
    }

At which point you should recieve a response of 

    {
      "id": 11,
      "user": 2,
      "created_at": "2024-11-17T18:42:19.886070Z"
    }
You now have an active conversation. Save your conversation ID and we will go ask a question to the chatbot. Return to the home page for the final endpoint


### Send a message
Now that your conversation is active, you can ask the chatbot a question. Navigate to the send message endpint from the homepage or click [here](http://127.0.0.1:8000/send_message/)

<img width="1260" alt="Send Message Endpoint" src="https://github.com/user-attachments/assets/3f9e5693-df2f-46e8-970c-f186382644a4">

In this endpoint you must provide the conversation ID of your conversation and then any question you want. If the question exists in the FAQs list we saw earlier, the chatbot will return the answer. Your request payload should look like

    {
      "conversation_id": "int",
      "question": "string"
    }

At this point you are free to use this conversation for as long as you want, asking as many questions as you want!

