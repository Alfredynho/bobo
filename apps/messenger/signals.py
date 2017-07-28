from constance import config
from constance.signals import config_updated
from django.dispatch import receiver

from apps.messenger.components.client import MessengerClient
from apps.messenger.components.requests import ContinousMenu, MenuItem, MessageRequest


@receiver(config_updated)
def constance_updated(updated_key, new_value, **kwargs):
    if updated_key == "CONTINUOS_MENU":
        if new_value:
            print("\n  HAY QUE ACTIVAR EL MENU \n")
            messenger = MessengerClient(access_token=config.PAGE_ACCESS_TOKEN)
            messenger.post_settings(
                ContinousMenu(
                    call_to_actions=[
                        MenuItem(
                            type=MenuItem.TYPE_POSTBACK,
                            title="HOLA",
                            payload="HOLA"
                        ),
                        MenuItem(
                            type=MenuItem.TYPE_POSTBACK,
                            title="MUNDO",
                            payload="MUNDO"
                        ),
                        MenuItem(
                            type=MenuItem.TYPE_WEB_URL,
                            title="TARJETAS",
                            url="https://oepbolivia.xyz/checkout",
                            webview_height_ratio=MenuItem.RATIO_FULL,
                            messenger_extensions=True
                        ),
                        MenuItem(
                            type=MenuItem.TYPE_WEB_URL,
                            title="AYUDA",
                            url="https://oepbolivia.xyz"
                        )
                    ]
                )
            )

        else:

        #     curl - X
        #     DELETE - H
        #     "Content-Type: application/json" - d
        #     '{
        #     "setting_type": "call_to_actions",
        #     "thread_state": "existing_thread"
        # }' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=PAGE_ACCESS_TOKEN"
            print("\n  HAY QUE DESACTIVAREL MENU \n")


    # print("SENDER: ", updated_key, " KEY: ", updated_key, " OLD_VALUE: ", old_value, " NEW_VALUE: ",new_value)
    # print("\n KEY: ", updated_key, " NEW_VALUE: ",new_value, " KWARGS: ", kwargs, "\n")