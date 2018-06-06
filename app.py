from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import datetime
from NbaScraper import ScrapeNba
from NbaAbbrevs import abbrevs

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""

    from_number = request.values.get('From', None)
    from_body = request.values.get('Body', None)

    current_date = datetime.datetime.today().strftime('%Y%m%d')
    game_info = ScrapeNba().get_data(current_date)
    in_msg = " ".join(from_body.split()).replace(" ", "").lower()

    resp = MessagingResponse()

    for k in abbrevs.keys():
        if in_msg in abbrevs[k]:
            team_name = abbrevs[k][2].capitalize()
            #team_name.capitalize()
            full_name = k if k == "LA Clippers" or k == "LA Lakers" else k + " " + team_name

            if k in game_info:
                a, b, c = game_info[k]
                #resp.message(a, '\n', b, '\n', c)
                resp.message(a + "\n" + b + "\n" + c)
                return str(resp)
            else:
                resp.message("The " + full_name + " have no game scheduled for today")
                return str(resp)

    resp.message("Not a valid team name")
    return str(resp)


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, port=5000, host="localhost")



