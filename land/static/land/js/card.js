function card(stripe_publishable_key, customer_email) {
    document.addEventListener("DOMContentLoaded", function(event){
        var stripe = Stripe(stripe_publishable_key);
        var elements = stripe.elements();

        var style = {
          base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
              color: '#aab7c4'
            }
          },
          invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
          }
        };

        // Create an instance of the card Element.
        var card = elements.create('card', {style: style});
        card.mount("#card-element");
    }); // DOMContentLoaded
}