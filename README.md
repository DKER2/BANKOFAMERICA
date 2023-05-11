# 1. Struture of our Resporitory 
1. Pricing Engine and ReportGenerator is in "Components" folder 
2. Market Data Producer and Trade Event Data Producer and Dashboard is in "Frontend" folder
3. Output after runing through the input file is in "output.json"
# 2. Run Our App
## 2.1 Run Frontend

Prerequisite: Nodejs >= 18.x
```
cd Frontend
```

```
npm install
```

```
npm start
```

## 2.2 Run Backend
```
cd Components
```

```
pip install flask, flask_cors
```

```
python app.py
```
## 2.3 Open output
```
Double click on "output.json" fie
```