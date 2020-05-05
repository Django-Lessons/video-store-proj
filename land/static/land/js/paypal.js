function _paypal(email) {
    document.addEventListener("DOMContentLoaded", function(event){
        paypal.Buttons({
          createSubscription: function(data, actions) {
            return actions.subscription.create({
              'plan_id': 'P-0W823661S01507548L2YU24Y',
              'subscriber': {
                'email_address': email
              },
            });
          },
          onApprove: function(data, actions) {
            alert('You have successfully created subscription ' + data.subscriptionID);
          }
        }).render('#paypal-button-container');
    }); // DOMContentLoaded
}