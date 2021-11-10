from tortoise.transactions import in_transaction

from bot.database.models import InviteCode


async def get_invite_code():
    """
    Получает первый не использованный код приглашения

    Returns:
        InviteCode: код приглашения
    """
    async with in_transaction():
        return InviteCode.filter(activated_by=None).first()


async def invalidate_invite_code(code: InviteCode, tg_id: int):
    """
    Помечает код приглашения невалидным

    Args:
        code: Код приглашения
        tg_id: ИД пользователя в Telegram

    Returns:
        InviteCode: код приглашения
    """
    async with in_transaction():
        return await InviteCode.filter(id=code.id).update(activated_by=tg_id)
