from textblob import TextBlob
from core.get_data import DataLoader
import datetime
import pandas as pd
from dbhelper.db_handler import DBHandler
import GetOldTweets3 as got


class sentiment:
    host = "localhost"
    port = 8086
    user = None
    password = None
    dbname = "mydb2"

    db = DBHandler(host, port, user, password, dbname)

    dl = DataLoader()

    def get_sentiment(self, ticker, company, startDate):

        db = self.db
        dl = self.dl

        startTime = datetime.datetime.strptime(startDate, "%Y-%m-%d")
        currentTime = datetime.datetime.today().strftime("%Y-%m-%d")
        currentTime = datetime.datetime.strptime(currentTime, "%Y-%m-%d")

        days = currentTime - startTime
        days = days.days

        output = db.QueryDataFromTable(
            "select * from " + ticker + " where time > now() - " + str(days) + "d"
        )

        df = dl.db_to_df(output)

        for i in range(len(df)):
            time = df.iloc[[i]].index[0]
            if time < datetime.datetime(2006, 6, 30):
                avg_polarity = 0.0
                avg_subjectivity = 0.0
                time = str(time)
                time = time.replace(" 00:00:00", "")
            else:
                time = str(time)
                time = time.replace(" 00:00:00", "")

                time2 = datetime.datetime.strptime(time, "%Y-%m-%d")
                next_day = str(time2 + datetime.timedelta(days=1))
                next_day = next_day.replace(" 00:00:00", "")

                tweetCriteria = (
                    got.manager.TweetCriteria()
                    .setQuerySearch(company)
                    .setSince(time)
                    .setUntil(next_day)
                    .setMaxTweets(0)
                )

                tweets = got.manager.TweetManager.getTweets(tweetCriteria)

                if len(tweets) == 0:
                    avg_polarity = 0.0
                    avg_subjectivity = 0.0

                else:
                    data = dict()
                    j = 0

                    for tweet in tweets:
                        if "http" not in tweet.text:
                            analysis = TextBlob(tweet.text)
                            data[j] = {
                                "polarity": analysis.sentiment.polarity,
                                "subjectivity": analysis.sentiment.subjectivity,
                            }
                            j += 1

                    polarity_total = 0
                    subjectivity_total = 0
                    invalid_data_counter = 0

                    for index in data:
                        if (
                            data[index]["polarity"] == 0
                            or data[index]["subjectivity"] == 0
                        ):
                            invalid_data_counter += 1

                        if invalid_data_counter == len(data):
                            avg_polarity = 0.0
                            avg_subjectivity = 0.0
                        else:
                            polarity_total = polarity_total + data[index]["polarity"]
                            subjectivity_total = (
                                subjectivity_total + data[index]["subjectivity"]
                            )

                    if len(data) - invalid_data_counter == 0:
                        avg_polarity = 0.0
                        avg_subjectivity = 0.0
                    else:
                        avg_polarity = polarity_total / (
                            len(data) - invalid_data_counter
                        )
                        avg_subjectivity = subjectivity_total / (
                            len(data) - invalid_data_counter
                        )

            output = db.GetRowFromTable(ticker, time)

            close = float(output[0][1])

            predict = float(output[0][2])

            data = [[time, close, predict, avg_polarity, avg_subjectivity]]
            df2 = pd.DataFrame(
                data,
                columns=["Date", "Close", "Prediction", "Polarity", "Subjectivity"],
            )

            df2["Date"] = pd.to_datetime(df2.Date, format="%Y-%m-%d")
            df2.index = df2["Date"]
            df2.drop(["Date"], inplace=True, axis=1)
            print(df2)

            db.DataFrameToDB(df2, ticker)
