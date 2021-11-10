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


async def user_got_code(tg_id: int) -> bool:
    """
    Проверяет, получал ли пользователь код

    Args:
        tg_id: ИД пользователя

    Returns:
        bool: Флаг получения пользователем кода
    """
    async with in_transaction():
        return bool(await InviteCode.get_or_none(activated_by=tg_id))
