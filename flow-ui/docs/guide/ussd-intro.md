# Introduction

According to Wikipedia USSD (Unstructured Supplementary Service Data) is a communications protocol used by GSM cellular telephones to communicate with the mobile network operator's computers. USSD can be used for WAP browsing, prepaid callback service, mobile-money services, location-based content services, menu-based information services, and as part of configuring the phone on the network.

The Basic USSD Flow usually take the approach below;

- User dials the provided USSD code. (This is done automatically for services that exist readily within the SIM Tool Kit)
- The request is forwarded to the MNO (Mobile Network Operator).
- The MNO routes the request through a gateway to the machine hosting the web application.
- The application processes the requests it receives and sends back a valid response.
- The feedback is processed by the MNO and sent back to the mobile phone.

## Getting Started

USSD is session driven, What does this mean ?, well whenever you dial \*XXX# a session with a unique Id is created and maintained to allow interaction of the end device and the remote API. [The session typically lasts 180s for most MNOs in Kenya ](https://help.africastalking.com/en/articles/1284071-what-is-the-duration-of-a-ussd-session-for-kenyan-telcos) it may be different for MNOs in other countries. As the developer, you'll need to keep track of the session and be cautious of the time limit to ensure that menus, as well as responses, are served faster and better to ensure a seamless user experience.
The MNO also lets you control the session, this is done by attaching CON or END at the start of every response

    CON: Means an intermediate menu or that the session is CONtinuing and hence will require user input
    END: This means the final menu and will trigger session termination i.e session is ENDing.

The above is properly documented on [Africas Talking's dev docs](https://developers.africastalking.com/docs/ussd/handle_sessions)
