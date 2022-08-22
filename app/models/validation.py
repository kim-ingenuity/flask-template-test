from core.main import db
from core.models import Model
# from core.settings import Config

class PrepaidAccountObj(Model):
    __tablename__ = 'PREPAID_ACCOUNTS'
    # __table_args__ = Config.CCB_PREPAID_DB_SCHEMA

    du_code = db.Column(db.String(5), nullable=False)
    juice_id = db.Column(db.String(15), nullable=True)
    acct_id = db.Column(db.String(15), primary_key=True, nullable=False)
    per_id = db.Column(db.String(15), nullable=False)
    sa_id = db.Column(db.String(15), nullable=False)
    sp_id = db.Column(db.String(15), nullable=False)
    premise_id = db.Column(db.String(15), nullable=False)
    meter_id = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(10), nullable=True)
    acct_name = db.Column(db.String(762), nullable=False)
    phone1 = db.Column(db.String(24), nullable=False)
    phone2 = db.Column(db.String(24), nullable=True)
    sms1 = db.Column(db.String(24), nullable=False)
    sms2 = db.Column(db.String(24), nullable=True)
    email = db.Column(db.String(70), nullable=False)
    address1 = db.Column(db.String(254), nullable=False)
    address2 = db.Column(db.String(254), nullable=True)
    city = db.Column(db.String(90), nullable=False)
    state = db.Column(db.String(6), nullable=False)
    zip = db.Column(db.String(12), nullable=False)
    serialnum = db.Column(db.String(16), nullable=False)
    badge_nbr = db.Column(db.String(30), nullable=False)
    addactiveread = db.Column(db.Numeric(10,2), nullable=False)
    meter_install_date = db.Column(db.Date, nullable=True)
    updated_on = db.Column(db.DateTime, nullable=False)
