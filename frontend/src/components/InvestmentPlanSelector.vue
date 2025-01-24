<template>
  <div class="investment-plan-selector">
    <h2>Select Your Investment Plan</h2>
    
    <!-- Risk Level Selector -->
    <div class="risk-selector">
      <h3>Choose Your Risk Tolerance</h3>
      <div class="risk-buttons">
        <button 
          v-for="level in riskLevels" 
          :key="level"
          @click="selectRiskLevel(level)"
          :class="{ active: selectedRiskLevel === level }"
        >
          {{ level.charAt(0).toUpperCase() + level.slice(1) }}
        </button>
      </div>
    </div>
    
    <!-- Investment Amount Slider -->
    <div class="investment-amount">
      <h3>Investment Amount</h3>
      <input 
        type="range" 
        v-model="investmentAmount"
        :min="minInvestment"
        :max="maxInvestment"
        step="500"
      />
      <span>{{ formatCurrency(investmentAmount) }}</span>
    </div>
    
    <!-- Investment Plan Cards -->
    <div class="investment-plans">
      <div 
        v-for="plan in filteredPlans" 
        :key="plan.id" 
        class="plan-card"
        @click="selectPlan(plan)"
        :class="{ selected: selectedPlan && selectedPlan.id === plan.id }"
      >
        <h4>{{ plan.name }}</h4>
        <p>{{ plan.description }}</p>
        
        <div class="plan-details">
          <div class="detail">
            <strong>Risk Level:</strong> 
            {{ plan.risk_level.charAt(0).toUpperCase() + plan.risk_level.slice(1) }}
          </div>
          <div class="detail">
            <strong>Expected Return:</strong> 
            {{ formatPercentage(plan.expected_return) }}
          </div>
          <div class="detail">
            <strong>Minimum Investment:</strong> 
            {{ formatCurrency(plan.min_investment) }}
          </div>
        </div>
        
        <div class="asset-allocation">
          <h5>Asset Allocation</h5>
          <div 
            v-for="(percentage, asset) in plan.asset_allocation" 
            :key="asset" 
            class="allocation-bar"
          >
            <span>{{ asset }}</span>
            <div 
              class="bar" 
              :style="{ width: `${percentage * 100}%` }"
            ></div>
            <span>{{ formatPercentage(percentage) }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Performance Simulation -->
    <div v-if="selectedPlan" class="performance-simulation">
      <h3>Performance Simulation</h3>
      <div v-if="simulationLoading">Loading simulation...</div>
      <div v-else-if="performanceSimulation" class="simulation-results">
        <div class="result">
          <strong>Mean Final Value:</strong> 
          {{ formatCurrency(performanceSimulation.mean_final_value) }}
        </div>
        <div class="result">
          <strong>Success Probability:</strong> 
          {{ formatPercentage(performanceSimulation.success_probability) }}
        </div>
        <div class="result">
          <strong>Value at Risk (95%):</strong> 
          {{ formatCurrency(performanceSimulation.value_at_risk_95) }}
        </div>
      </div>
    </div>
    
    <!-- Action Buttons -->
    <div class="action-buttons">
      <button 
        @click="proceedWithPlan" 
        :disabled="!selectedPlan"
      >
        Proceed with {{ selectedPlan ? selectedPlan.name : 'Plan' }}
      </button>
      <button @click="resetSelection">Reset Selection</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'InvestmentPlanSelector',
  data() {
    return {
      riskLevels: ['low', 'medium', 'high'],
      selectedRiskLevel: null,
      investmentAmount: 5000,
      minInvestment: 1000,
      maxInvestment: 100000,
      investmentPlans: [],
      selectedPlan: null,
      performanceSimulation: null,
      simulationLoading: false
    };
  },
  computed: {
    filteredPlans() {
      return this.investmentPlans.filter(plan => 
        (!this.selectedRiskLevel || plan.risk_level === this.selectedRiskLevel) &&
        plan.min_investment <= this.investmentAmount
      );
    }
  },
  methods: {
    async fetchInvestmentPlans() {
      try {
        const response = await axios.get('/api/investment-plans');
        this.investmentPlans = response.data.investment_plans;
      } catch (error) {
        console.error('Failed to fetch investment plans', error);
      }
    },
    selectRiskLevel(level) {
      this.selectedRiskLevel = this.selectedRiskLevel === level ? null : level;
    },
    async selectPlan(plan) {
      this.selectedPlan = plan;
      this.simulationLoading = true;
      
      try {
        const response = await axios.get(
          `/api/investment-plans/${plan.id}/performance`, 
          { params: { investment_amount: this.investmentAmount } }
        );
        this.performanceSimulation = response.data.performance;
      } catch (error) {
        console.error('Failed to simulate performance', error);
      } finally {
        this.simulationLoading = false;
      }
    },
    proceedWithPlan() {
      if (this.selectedPlan) {
        this.$emit('plan-selected', {
          plan: this.selectedPlan,
          investmentAmount: this.investmentAmount
        });
      }
    },
    resetSelection() {
      this.selectedRiskLevel = null;
      this.selectedPlan = null;
      this.performanceSimulation = null;
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(value);
    },
    formatPercentage(value) {
      return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(value);
    }
  },
  mounted() {
    this.fetchInvestmentPlans();
  }
}
</script>

<style scoped>
.investment-plan-selector {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f4f4f4;
  border-radius: 8px;
}

.risk-buttons button {
  margin: 0 10px;
  padding: 10px 20px;
  background-color: #e0e0e0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.risk-buttons button.active {
  background-color: #4CAF50;
  color: white;
}

.investment-plans {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.plan-card {
  flex: 1;
  min-width: 250px;
  border: 1px solid #ddd;
  padding: 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.plan-card:hover, .plan-card.selected {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-color: #4CAF50;
}

.allocation-bar {
  display: flex;
  align-items: center;
  margin: 5px 0;
}

.allocation-bar .bar {
  background-color: #4CAF50;
  height: 10px;
  margin: 0 10px;
}

.action-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.action-buttons button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.action-buttons button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
