from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.utils.security import admin_required
from investment_plans import InvestmentPlanManager
from investment_plan_validator import InvestmentPlanValidator

investment_plans_admin_bp = Blueprint('investment_plans_admin', __name__)
plan_manager = InvestmentPlanManager()
plan_validator = InvestmentPlanValidator()

@investment_plans_admin_bp.route('/investment-plans', methods=['POST'])
@login_required
@admin_required
def create_investment_plan():
    """
    Create a new investment plan
    
    Requires admin authentication
    """
    data = request.get_json()
    
    # Validate input data
    validation_result = plan_validator.validate_investment_plan(data)
    
    if not validation_result['is_valid']:
        return jsonify({
            'status': 'error',
            'errors': validation_result['errors']
        }), 400
    
    try:
        investment_plan = plan_manager.create_investment_plan(**data)
        return jsonify({
            'status': 'success',
            'investment_plan': investment_plan
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@investment_plans_admin_bp.route('/investment-plans', methods=['GET'])
@login_required
@admin_required
def list_investment_plans():
    """
    Retrieve all investment plans
    
    Requires admin authentication
    """
    risk_level = request.args.get('risk_level')
    min_investment = request.args.get('min_investment', type=float)
    
    try:
        investment_plans = plan_manager.get_investment_plans(
            risk_level=risk_level,
            min_investment=min_investment
        )
        return jsonify({
            'status': 'success',
            'investment_plans': investment_plans
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@investment_plans_admin_bp.route('/investment-plans/<int:plan_id>', methods=['PUT'])
@login_required
@admin_required
def update_investment_plan(plan_id):
    """
    Update an existing investment plan
    
    Requires admin authentication
    """
    data = request.get_json()
    
    # Validate input data
    validation_result = plan_validator.validate_investment_plan(data)
    
    if not validation_result['is_valid']:
        return jsonify({
            'status': 'error',
            'errors': validation_result['errors']
        }), 400
    
    try:
        updated_plan = plan_manager.update_investment_plan(plan_id, **data)
        return jsonify({
            'status': 'success',
            'investment_plan': updated_plan
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@investment_plans_admin_bp.route('/investment-plans/<int:plan_id>/performance', methods=['GET'])
@login_required
@admin_required
def simulate_investment_plan_performance(plan_id):
    """
    Simulate investment plan performance
    
    Requires admin authentication
    """
    investment_amount = request.args.get('investment_amount', type=float, default=10000)
    
    try:
        # Retrieve investment plan
        plans = plan_manager.get_investment_plans()
        plan = next((p for p in plans if p['id'] == plan_id), None)
        
        if not plan:
            return jsonify({
                'status': 'error',
                'message': 'Investment plan not found'
            }), 404
        
        # Simulate performance
        performance = plan_validator.simulate_investment_performance(
            plan, 
            investment_amount=investment_amount
        )
        
        return jsonify({
            'status': 'success',
            'performance': performance
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@investment_plans_admin_bp.route('/investment-plans/<int:plan_id>/recommendations', methods=['GET'])
@login_required
@admin_required
def get_investment_plan_recommendations(plan_id):
    """
    Get recommendations for an investment plan
    
    Requires admin authentication
    """
    try:
        # Retrieve investment plan
        plans = plan_manager.get_investment_plans()
        plan = next((p for p in plans if p['id'] == plan_id), None)
        
        if not plan:
            return jsonify({
                'status': 'error',
                'message': 'Investment plan not found'
            }), 404
        
        # Get recommendations
        recommendations = plan_validator.recommend_plan_adjustments(plan)
        
        return jsonify({
            'status': 'success',
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
