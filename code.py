from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask_cors import CORS

# Create the Flask app first
app = Flask(__name__)
CORS(app)

# 🛠 Replace with your actual RDS connection info
username = 'admin'  # your RDS username
password = 'TeamBharath'  # your RDS password
host = 'database-1.cuxe6qw082l3.us-east-1.rds.amazonaws.com'  # your RDS endpoint
database = 'flaskapp'  # your RDS DB name

# MySQL connection string using PyMySQL driver
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy AFTER app is created and configured
db = SQLAlchemy(app)

# Define the table/model
class RecommendationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_type = db.Column(db.String(50))
    input_data = db.Column(db.Text)
    recommendation = db.Column(db.Text)
    benefits = db.Column(db.Text)
    example = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables (run once)
with app.app_context():
    db.create_all()

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    rec_type = data.get('type')
    recommendation = ""
    benefits = []
    example = ""

    # Recommendation Logic (unchanged)
    if rec_type == "cloud_service_optimization":
        workload = data.get('workload')
        budget = data.get('budget')
        if workload == "compute-intensive" and budget == "low":
            recommendation = "Use AWS Fargate to run containers without managing servers."
            benefits = ["No server management", "Cost-effective", "Auto-scaling"]
            example = "A video analytics firm switched to Fargate and reduced compute costs by 35%."
        elif workload == "event-driven":
            recommendation = "Use AWS Lambda to run code in response to events."
            benefits = ["Pay-per-use", "Scalable", "Event-triggered"]
            example = "A photo app used Lambda for file uploads and saved on idle compute."
        else:
            recommendation = "Use EC2 with auto-scaling for general-purpose workloads."
            benefits = ["Customizable", "Flexible pricing", "Supports any OS"]
            example = "An internal tool used EC2 with spot instances to cut 50% cost."

    elif rec_type == "tech_stack":
        traffic = data.get('traffic')
        if traffic == "low":
            recommendation = "Use serverless stack: Lambda + DynamoDB + S3."
            benefits = ["Low cost", "No server maintenance", "Auto-scaling"]
            example = "A portfolio website used this stack with near-zero costs."
        else:
            recommendation = "Use Node.js backend with RDS and React for scalable apps."
            benefits = ["Mature ecosystem", "High performance", "Great for SPAs"]
            example = "A SaaS startup scaled easily with Node + RDS + React."

    elif rec_type == "saas_bundle":
        size = data.get('company_size')
        if size == "startup":
            recommendation = "Use HubSpot (CRM), Freshdesk (Support), and Mixpanel (Analytics)."
            benefits = ["Startup-friendly pricing", "Quick setup", "Integration-ready"]
            example = "A 5-person SaaS team automated support and CRM with these tools."
        else:
            recommendation = "Use Salesforce, Zendesk, and Segment for enterprise operations."
            benefits = ["Enterprise-grade features", "Scalability", "Security"]
            example = "A fintech company scaled sales with this bundle."

    elif rec_type == "cost_optimization":
        recommendation = "Enable Cost Explorer, use Auto Scaling, and buy Reserved Instances."
        benefits = ["Save up to 72%", "Avoid unused resources", "Predictable billing"]
        example = "A retail firm saved $10K/month by downsizing EC2s and using RIs."

    elif rec_type == "marketplace":
        industry = data.get('industry')
        recommendation = f"Based on industry: {industry}, use DevOps consulting + observability tools."
        benefits = ["Faster delivery", "Better monitoring", "Expert help"]
        example = "An eCommerce firm used internal marketplace DevOps to improve CI/CD."

    elif rec_type == "security_engine":
        data_type = data.get('data_type')
        recommendation = f"Use AWS WAF, GuardDuty, IAM policies tailored for {data_type} data."
        benefits = ["Protection from attacks", "Secure access", "Compliance support"]
        example = "A healthcare firm secured PHI using WAF and GuardDuty with IAM roles."

    else:
        return jsonify({"error": "Unknown recommendation type"}), 400

    # Save to DB
    log = RecommendationLog(
        input_type=rec_type,
        input_data=str(data),
        recommendation=recommendation,
        benefits=str(benefits),
        example=example
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "recommendation": recommendation,
        "benefits": benefits,
        "example": example
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  # <-- fixed missing parenthesis
