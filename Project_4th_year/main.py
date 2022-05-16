from website import create_app
import cvtest
app = create_app()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

'''vid = cvtest.video()

vid.run()

capture = cvtest.search_send()

capture.run()'''