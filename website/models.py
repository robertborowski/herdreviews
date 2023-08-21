# ------------------------ imports start ------------------------
from email.policy import default
from website import db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from website import secret_key_ref
# ------------------------ imports end ------------------------

# ------------------------ individual model start ------------------------
# Note: models vs tables: https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy
class UserObj(db.Model, UserMixin):   # Only the users object inherits UserMixin, other models do NOT!
  # ------------------------ general start ------------------------
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150))
  password = db.Column(db.String(150))
  name = db.Column(db.String(150))
  company_name = db.Column(db.String(150))
  group_id = db.Column(db.String(150))
  fk_stripe_customer_id = db.Column(db.String(150))
  # ------------------------ general start ------------------------
  # ------------------------ candidates start ------------------------
  fk_stripe_subscription_id = db.Column(db.String(150))
  # ------------------------ candidates end ------------------------
  # ------------------------ employees start ------------------------
  employees_fk_stripe_subscription_id = db.Column(db.String(150))
  # ------------------------ employees end ------------------------
  verified_email = db.Column(db.Boolean, default=False)
  signup_product = db.Column(db.String(150))
  last_name = db.Column(db.String(150))

  def get_reset_token_function(self, expires_sec=1800):
    serializer_token_obj = Serializer(secret_key_ref, expires_sec)
    return serializer_token_obj.dumps({'dump_load_user_id': self.id}).decode('utf-8')

  @staticmethod
  def verify_reset_token_function(token_to_search_for):
    serializer_token_obj = Serializer(secret_key_ref)
    try:
      dl_user_id_from_token = serializer_token_obj.loads(token_to_search_for)['dump_load_user_id']
    except:
      return None
    return UserObj.query.get(dl_user_id_from_token)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class UserAttributesObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_user_id = db.Column(db.String(150))
  product = db.Column(db.String(150))
  anonymous_status = db.Column(db.Boolean, default=False)
  attribute_code = db.Column(db.String(150))
  attribute_response = db.Column(db.String(150))
  attribute_year = db.Column(db.Integer)
  attribute_month = db.Column(db.Integer)
  attribute_day = db.Column(db.Integer)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class EmailSentObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  from_user_id_fk = db.Column(db.String(150))
  to_email = db.Column(db.String(150))
  subject = db.Column(db.String(1000))
  body = db.Column(db.String(5000))
# ------------------------ individual model end ------------------------

"""
# ------------------------ individual model start ------------------------
class EmailCollectObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150))
  source = db.Column(db.String(20))
  unsubscribed = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------
# ------------------------ individual model start ------------------------
class EmailDeletedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150), primary_key=True)
  uuid_archive = db.Column(db.String(150), primary_key=True)
# ------------------------ individual model end ------------------------
# ------------------------ individual model start ------------------------
class EmailScrapedObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  email = db.Column(db.String(150), unique=True)
  unsubscribed = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------
"""

# ------------------------ individual model start ------------------------
class StripeCheckoutSessionObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_checkout_session_id = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
  status = db.Column(db.String(20))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class StripePaymentOptionsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  candence = db.Column(db.String(10))
  price = db.Column(db.Float)
  fk_stripe_price_id = db.Column(db.String(150))
  name = db.Column(db.String(20))
  fk_stripe_price_id_testing = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class BlogPollingObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  title = db.Column(db.String(150))
  details = db.Column(db.String(150))
  aws_image_url = db.Column(db.String(150))
  status = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class PlatformsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  name = db.Column(db.String(150))
  status = db.Column(db.Boolean, default=False)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class PollsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  type = db.Column(db.String(150))
  fk_show_id = db.Column(db.String(150))
  question = db.Column(db.String(150))
  answer_choices = db.Column(db.String(1000))
  written_response_allowed = db.Column(db.Boolean, default=True)
  topics = db.Column(db.String(150))
  status_approved = db.Column(db.Boolean, default=False)
  status_removed = db.Column(db.Boolean, default=False)
  fk_user_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class PollsAnsweredObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_show_id = db.Column(db.String(150))
  fk_poll_id = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
  poll_answer_submitted = db.Column(db.String(500))
  written_answer_submitted = db.Column(db.String(150))
  status_answer_anonymous = db.Column(db.Boolean, default=False)
  poll_vote_updown_question = db.Column(db.Boolean)
  poll_vote_updown_feedback = db.Column(db.Boolean)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class PollsStandInObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_show_id = db.Column(db.String(150))
  fk_poll_id = db.Column(db.String(150))
  standin_key = db.Column(db.String(150))
  standin_values = db.Column(db.String(1000))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ShowsFollowingObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_platform_id = db.Column(db.String(150))
  fk_show_id = db.Column(db.String(150))
  fk_user_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ShowsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  name = db.Column(db.String(150))
  description = db.Column(db.String(1000))
  topics = db.Column(db.String(150))
  fk_platform_id = db.Column(db.String(150))
  status = db.Column(db.Boolean, default=False)
  platform_reference_id = db.Column(db.String(150))
  platform_image_large = db.Column(db.String(150))
  platform_image_medium = db.Column(db.String(150))
  platform_image_small = db.Column(db.String(150))
  platform_url = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ShowsAttributesObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_show_id = db.Column(db.String(150))
  attribute_key = db.Column(db.String(150))
  attribute_value = db.Column(db.String(150))
  attribute_note = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class ShowsQueueObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_platform_id = db.Column(db.String(150))
  platform_reference_id = db.Column(db.String(150))
  name = db.Column(db.String(150))
  description = db.Column(db.String(1000))
  img_large = db.Column(db.String(150))
  img_medium = db.Column(db.String(150))
  img_small = db.Column(db.String(150))
  show_url = db.Column(db.String(150))
  fk_show_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class RedditPostsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  community = db.Column(db.String(100))
  title = db.Column(db.String(300))
  total_votes = db.Column(db.Integer)
  total_comments = db.Column(db.Integer)
  post_url = db.Column(db.String(300))
  total_upvotes = db.Column(db.Integer)
  upvote_ratio = db.Column(db.Float)
  total_views = db.Column(db.Integer)
  poll_data_obj = db.Column(db.String(1000))
  post_removed = db.Column(db.Boolean)
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class RedditCommentsObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_reddit_post_id = db.Column(db.String(150))
  author = db.Column(db.String(150))
  comment = db.Column(db.String(1000))
  upvotes = db.Column(db.Integer)
  downvotes = db.Column(db.Integer)
  created_at = db.Column(db.DateTime(timezone=True))
  comment_url = db.Column(db.String(300))
# ------------------------ individual model end ------------------------

# ------------------------ individual model start ------------------------
class RedditMappingObj(db.Model):
  id = db.Column(db.String(150), primary_key=True)
  created_timestamp = db.Column(db.DateTime(timezone=True))
  fk_poll_id = db.Column(db.String(150))
  fk_reddit_post_id = db.Column(db.String(150))
# ------------------------ individual model end ------------------------