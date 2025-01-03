import requests
from decouple import config


class DiscordBot:
    """
    Will send msg to discord regarding the order statuses.
    """

    def __init__(self):
        self.bot_id = config("discord_bot_id")
        self.channel_id = config("discord_channel_id")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bot {self.bot_id}",
        }

    def send_msg(self, order_id: int, action: str):
        action_msg_mapper = {
            "dispatch": "is collected and dispatched to desired location."
            f" By making PUT request on this link: {config('dns')}:/dispatcher/approve-shipped/{order_id} you will changed the order status to shipped!",
            "payment_success": "is successfully payed by user!",
            "payment_failed": "failed to be payed by user! Please contact him!",
        }
        json_payload = {
            "content": f"Order ID: {order_id} {action_msg_mapper[action]}",
        }
        requests.post(
            f"https://discord.com/api/v9/channels/{self.channel_id}/messages",
            json=json_payload,
            headers=self.headers,
        )
