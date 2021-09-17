from chainBid.celery import app


@app.task
def start_auction(instance):
    """
    Valutare il try/except
    import logging
    logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)
    """

    instance.toggle_status()

# from django.contrib.auth import get_user_model
# UserModel = get_user_model()
# user = UserModel.objects.get(pk=user_id)
