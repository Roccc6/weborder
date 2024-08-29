from App import create_app
app = create_app()
if __name__ == '__main__':
    # 允许外网访问，并且开启debug模式
    app.run(host='0.0.0.0', debug=True, port=5000)