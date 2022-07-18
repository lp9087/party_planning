import queue

from count.models import Member, Party


class Role:

    def __init__(self, member: Member, rest_of_money: float):
        self.member = member
        self.rest_of_money = rest_of_money

    def change_rest_of_money(self, money: float) -> None:
        self.rest_of_money = self.rest_of_money - money


class Receiver(Role):
    pass


class Sender(Role):
    pass


class SenderReceiver:
    def __init__(self, sender: Sender, receiver: Receiver, money: float):
        self.sender = sender
        self.receiver = receiver
        self.money = money

    def to_json(self):
        return {
            "sender": self.sender.member.name,
            "receiver": self.receiver.member.name,
            "money": self.money
        }

    def __str__(self):
        return f"{self.sender.member.name} отправил {self.receiver.member.name} {self.money} рублей"


def link_sender_receiver(sender: Sender, receiver: Receiver) -> SenderReceiver:
    send_money = min(sender.rest_of_money, receiver.rest_of_money)
    sender.change_rest_of_money(send_money)
    receiver.change_rest_of_money(send_money)
    return SenderReceiver(sender, receiver, send_money)


def party_handle(party: Party) -> [SenderReceiver]:
    procest_member = []
    receiver_queue = queue.Queue()
    sender_queue = queue.Queue()

    for member in party.dateparty.all():
        ###Для ресиверов
        if member.party_summary_purchases > member.get_member_usage_purchase():
            rest_of_money = member.party_summary_purchases - member.get_member_usage_purchase()
            receiver = Receiver(member, rest_of_money)

            while sender_queue.qsize() > 0 and receiver.rest_of_money != 0:
                sender = sender_queue.get()
                linked_sender_receiver = link_sender_receiver(sender, receiver)
                procest_member.append(linked_sender_receiver)

                if sender.rest_of_money > 0:
                    sender_queue.put(sender)

            if sender_queue.qsize() == 0:
                receiver_queue.put(receiver)

        ###Для сендеров
        elif member.party_summary_purchases < member.get_member_usage_purchase():
            rest_of_money = member.get_member_usage_purchase() - member.party_summary_purchases
            sender = Sender(member, rest_of_money)

            while receiver_queue.qsize() > 0 and sender.rest_of_money != 0:
                receiver = receiver_queue.get()
                linked_sender_receiver = link_sender_receiver(sender, receiver)
                procest_member.append(linked_sender_receiver)

                if receiver.rest_of_money > 0:
                    receiver_queue.put(receiver)

            if receiver_queue.qsize() == 0:
                sender_queue.put(sender)

    return procest_member
