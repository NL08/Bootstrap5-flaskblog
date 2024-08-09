import stripe
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.payment.forms import EmailForm

payment = Blueprint('payment', __name__, template_folder='templates')
# import db from  folder in __init__.py.
from app import db
from app.models import Payments

'''
# This is before the table was created.
products = {
    'donations': 
    {
        'name': 'Donation for the site',
        'price': 500, # 500 is = 5.00 , how do I use a counter? Answer turn into a table in a database
    }
}
'''
from app.payment.functions import add_foreign_key
@payment.route('/donations', methods = ['POST', 'GET'])
def donations():
    form = EmailForm()
    if form.validate_on_submit():
        ''' 
        Start off as a decimal float then you mulitply by 100 to get the cents. An ex int ex .55 then get 55.0,
        then convert from float to int then to string because request.form uses str/strings.
        '''
        flash('price_of_donation_form') 
        if not request.form["number"]: # empty form
            error = 'Please type in an amount to donate.'
            return render_template('stripe_payment/donations.html', form=form, title='Give donations', error=error)        
                
        # The reason you do the converting from a decimal float to a int because sql can't store decimals. 
        price_of_donation_form = str(int(float(request.form["number"]) *100) ) # Make global variable?
        email_form = form.email.data
        print(email_form)
        add_payment_db = Payments(price_of_donation=price_of_donation_form, item_name='Donate', email=email_form) 
        db.session.add(add_payment_db) 
        db.session.commit()
          
    
        payment_id = add_payment_db.id
        add_foreign_key(email_form)
        # I need to query id because that is the only thing that is unique in the db 
        payment_db = db.one_or_404(db.select(Payments).filter_by(id=payment_id))
        # 307 allows the redirects to redirect to a POST request           
        return redirect(url_for('payment.order', payment_db_id=payment_db.id), code=307)
    
    error = None # empty, the if statement won't work   
    return render_template('stripe_payment/donations.html', form=form, title='Give donations', error=error)

# Is the route secure with just id?
@payment.route('/order/<payment_db_id>', methods=['POST'])
def order(payment_db_id):
    # I need to query id because that is the only thing that is unique in the db 
    payment_db = db.one_or_404(db.select(Payments).filter_by(id=payment_db_id))
    '''
    you can only purchase one product at a time, but since line_items is a list, 
    you can select and buy multiple products if you add a shopping cart interface
    ''' 
    checkout_session = stripe.checkout.Session.create(   
        # The line_items argument specifies the product that the user wishes to buy.
        line_items=[
            {
                'price_data': {
                    'product_data': {
                        'name': payment_db.item_name, 
                    },
                 
                    # automatically converts to decimals/float
                    'unit_amount': payment_db.price_of_donation,
                    'currency': 'usd',
                },
                'quantity': 1,
            },
        ],         
        # prefill the email input in the form.
        # I use this so I don't have 2 different emails in 2 different forms.  
        customer_email=payment_db.email,
        # payment_method_types argument allows what payment you want/allow.
        payment_method_types=['card'],
        # mode specifies what type of payment you want. An example is payment is a one time payment. 
        mode='payment',
        # stripe will redirect to one of these pages upon the form completion. How?
        success_url=request.host_url + 'order/success',
        cancel_url=request.host_url + 'order/cancel',
    )
    return redirect(checkout_session.url)
 



@payment.route('/order/success')
def success():
    return render_template('success.html')


@payment.route('/order/cancel')
def cancel():
    # send email 
    return render_template('cancel.html')

 




    