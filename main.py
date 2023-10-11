import os
# Use the package we installed
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token='',
    signing_secret=''
)

@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
            {
                "type": "section",
                "block_id": "sectionBlockOnlyPlainText",
                "text": {
                    "type": "plain_text",
                    "text": "This is a plain text section block.",
                    "emoji": True
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "datepicker",
                        "initial_date": "1990-04-28",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                            "emoji": True
                        },
                        "action_id": "actionId-0"
                    },
                    {
                        "type": "datepicker",
                        "initial_date": "1990-04-28",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a date",
                            "emoji": True
                        },
                        "action_id": "actionId-1"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Get My Report!"
                        },
                        "action_id": "button_1"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Report ",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "block_id": "sectionBlockWithUsersSelect",
                "text": {
                    "type": "mrkdwn",
                    "text": "Select users"
                },
                "accessory": {
                    "type": "users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user",
                        "emoji": True
                    },
                }
            },
            {
                "type": "section",
                "block_id": "sectionBlockWithStaticSelect",
                "text": {
                    "type": "mrkdwn",
                    "text": "Select Type"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select type from ",
                        "emoji": True
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*here1*",
                                "emoji": True
                            },
                            "value": "herevalue1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*here2*",
                                "emoji": True
                            },
                            "value": "hereValue2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*here3*",
                                "emoji": True
                            },
                            "value": "herevalue3"
                        }
                    ],
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Comments",
                    "emoji": True
                }
            }
        ]
      }
    )

  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")



def button_confirm(client, logger):
    logger.info("hit confirm!")

    try:
        client.chat_postMessage(
            channel=os.environ.get("SLACK_CHANNEL"),
            blocks='Hello from app',
        )
        print(f"Sending blocks ...")
    except Exception as e:
        logger.error("Error confirming message: {}".format(e))
    pass

@app.action("actionId-1")
def handle_all_actions(ack, action, logger):
    print('Is this even being called?')
    ack()


@app.action("actionId-0")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)


@app.action("button_1")
def update_message(ack, body, client):
    print('something happened')
    ack()
    print(body)
    print(client)

    res = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "modal-identifier",
            "title": {
                "type": "plain_text",
                "text": "Just a modal"
            },
            "blocks": [
                {
                    "type": "section",
                    "block_id": "section-identifier",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*report!"
                    },

                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Date*"
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Type*"
                        },
                        {
                            "type": "plain_text",
                            "text": "2023-01-01",
                            "emoji": True
                        },
                        {
                            "type": "mrkdwn",
                            "text": "foo"
                        },
                        {
                            "type": "plain_text",
                            "text": "2023-01-10",
                            "emoji": True
                        },
                        {
                            "type": "mrkdwn",
                            "text": "bar"
                        }
                    ]
                }
            ],
        }
    )


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))