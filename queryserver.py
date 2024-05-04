import numpy as np
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import text
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Aaudut%40123@localhost/pneumonia'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('server.html')

@app.route('/execute_query', methods=['POST'])
def execute_query():
    if request.method == 'POST':
        
     query = request.form['query']
     print(query)
     result = execute_sql(query)
    def laplace_mechanism(query_result, sensitivity, epsilon):
        try: 
          scale = sensitivity / epsilon
          total_noise = 0
          for x in range(99):
              noise = np.random.laplace(0, scale)
            #   print(noise)
              if noise > 0 and total_noise>0:
                total_noise = total_noise + noise

              elif noise>0 and total_noise < 0:
                  total_noise = -1*total_noise + noise

              elif noise < 0 and total_noise > 0:
                 total_noise = -1*total_noise + noise

              else:
                  total_noise = total_noise + noise

          total_noise = total_noise/100
          total_noise = round(total_noise)      
          print(total_noise)
          noisy_result = query_result[0][0] + total_noise
          return noisy_result
        except Exception as e:
            return f"Error : {str(e)}" 
  
    return render_template('server.html', query=query, result = result[0][0],noisy_result=laplace_mechanism(result,1,0.6 ))

def execute_sql(query):
     try:
        with db.engine.begin() as conn:
         result = conn.execute(text(query)) 
         conn.commit() 
        return result.fetchall()
     
     except Exception as e:
        return f"Error executing query: {str(e)}"

if __name__ == '__main__':
        app.run(debug=True, port=3000)