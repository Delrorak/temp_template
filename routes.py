from config import app
from controller_functions import route_to_index, register_new_user, login_process, user_dashboard, logout, edit_account, update_user, add_quote, user_posted_quotes, delete_quote, likes

app.add_url_rule('/', view_func=route_to_index)

app.add_url_rule('/register', view_func=register_new_user, methods=['POST'])

app.add_url_rule('/login', view_func=login_process, methods=['POST'])

app.add_url_rule('/user_dashboard/<id>', view_func=user_dashboard)

app.add_url_rule('/logout',view_func=logout)

app.add_url_rule('/edit_account/<id>', view_func=edit_account)

app.add_url_rule('/update_user/<id>', view_func=update_user, methods=['POST'])

app.add_url_rule('/add_quote/<id>', view_func=add_quote, methods=['POST'])

app.add_url_rule('/user_posted_quotes/<id>,<user_that_posted_id>', view_func=user_posted_quotes)

app.add_url_rule('/delete_quote/<user_id>,<quote_id>',view_func=delete_quote, methods=['POST'])

app.add_url_rule('/likes/<user_id>,<quote_id>',view_func=likes, methods=['POST'])