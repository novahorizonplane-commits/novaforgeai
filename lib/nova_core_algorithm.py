"""
NOVA CORE ALGORITHM v1.0
Advanced Risk Analysis & Decision Engine for NovaForgeAI Platform

Purpose:
  Analyzes critical platform metrics to make intelligent approve/review/reject/escalate decisions
  Prevents fraud, ensures network health, maintains treasury integrity, and optimizes governance

Real-time Analysis:
  - Fraud Risk Detection
  - Network Congestion Monitoring
  - Treasury Health Assessment
  - Governance Activity Tracking
  - Validator Performance Analysis
  - Staking Activity Monitoring
  - Liquidity Level Tracking

Output Decisions:
  - APPROVE: Automatic approval based on low-risk metrics
  - REVIEW: Flag for human review if metrics are uncertain
  - REJECT: Automatic rejection for high-risk transactions
  - ESCALATE: Route to senior admin/security team for investigation
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum
import json
from datetime import datetime, timedelta

# ============================================
# ENUMS & CONSTANTS
# ============================================

class Decision(Enum):
    APPROVE = "approve"
    REVIEW = "review"
    REJECT = "reject"
    ESCALATE = "escalate"

class RiskLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# Risk thresholds (0-100 scale)
FRAUD_RISK_THRESHOLD_LOW = 20
FRAUD_RISK_THRESHOLD_MEDIUM = 50
FRAUD_RISK_THRESHOLD_HIGH = 75

CONGESTION_THRESHOLD_LOW = 40  # % of max capacity
CONGESTION_THRESHOLD_HIGH = 80

TREASURY_HEALTH_THRESHOLD_CRITICAL = 30  # % of minimum required
TREASURY_HEALTH_THRESHOLD_WARNING = 60

VALIDATOR_UPTIME_THRESHOLD = 95  # %
STAKING_CONCENTRATION_THRESHOLD = 40  # % of total stake

# ============================================
# DATA STRUCTURES
# ============================================

@dataclass
class TransactionMetrics:
    """Input metrics for a transaction/proposal being evaluated"""
    transaction_id: str
    transaction_type: str  # payment, token_creation, contract_deployment, etc.
    amount: float
    user_history_score: float  # 0-100, based on past behavior
    ip_new: bool
    wallet_age_days: int
    previous_transactions: int
    timestamp: datetime

@dataclass
class NetworkMetrics:
    """Current network health metrics"""
    pending_transactions: int
    max_block_capacity: int
    average_gas_price: float
    block_time_seconds: float
    network_participants: int
    active_validators: int

@dataclass
class TreasuryMetrics:
    """Treasury and fiscal health"""
    total_balance: float
    required_minimum: float
    monthly_burn_rate: float
    monthly_inflow: float
    reserve_ratio: float  # balance / monthly_burn_rate

@dataclass
class GovernanceMetrics:
    """Governance health"""
    proposal_count_7days: int
    voter_participation_rate: float
    proposal_avg_execution_time_hours: float
    active_governance_token_holders: int

@dataclass
class ValidatorMetrics:
    """Validator network health"""
    validator_count: int
    average_uptime: float
    max_stake_concentration: float  # % of top validator
    slashing_incidents_7days: int
    avg_commission_rate: float

@dataclass
class StakingMetrics:
    """Staking activity"""
    total_staked: float
    staking_ratio: float  # % of total supply
    daily_unstaking_requests: int
    top_validator_concentration: float
    avg_delegation_size: float

@dataclass
class LiquidityMetrics:
    """Market liquidity health"""
    dex_volume_24h: float
    bid_ask_spread: float  # %
    slippage_1m_trade: float  # %
    liquidity_provider_count: int
    min_liquidity_threshold: float

# ============================================
# NOVA CORE ALGORITHM
# ============================================

class NovaCorAlgorithm:
    """
    Core decision engine for NovaForgeAI platform
    Implements multi-factor risk analysis and intelligent approval routing
    """

    def __init__(self):
        self.analysis_history: List[Dict] = []
        self.decision_log: List[Dict] = []

    def analyze_and_decide(
        self,
        transaction: TransactionMetrics,
        network: NetworkMetrics,
        treasury: TreasuryMetrics,
        governance: GovernanceMetrics,
        validators: ValidatorMetrics,
        staking: StakingMetrics,
        liquidity: LiquidityMetrics,
    ) -> Tuple[Decision, Dict]:
        """
        Main decision engine - analyzes all metrics and returns decision
        
        Returns:
            (Decision, detailed_analysis_dict)
        """
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "transaction_id": transaction.transaction_id,
            "transaction_type": transaction.transaction_type,
            "metrics": {}
        }

        # Calculate individual risk scores (0-100)
        fraud_risk = self._calculate_fraud_risk(transaction)
        congestion_risk = self._calculate_congestion_risk(network)
        treasury_risk = self._calculate_treasury_risk(treasury)
        governance_risk = self._calculate_governance_risk(governance)
        validator_risk = self._calculate_validator_risk(validators)
        staking_risk = self._calculate_staking_risk(staking)
        liquidity_risk = self._calculate_liquidity_risk(liquidity)

        # Store individual scores
        analysis["metrics"] = {
            "fraud_risk": fraud_risk,
            "congestion_risk": congestion_risk,
            "treasury_risk": treasury_risk,
            "governance_risk": governance_risk,
            "validator_risk": validator_risk,
            "staking_risk": staking_risk,
            "liquidity_risk": liquidity_risk,
        }

        # Calculate weighted overall risk
        overall_risk = self._calculate_overall_risk(
            fraud_risk,
            congestion_risk,
            treasury_risk,
            governance_risk,
            validator_risk,
            staking_risk,
            liquidity_risk,
            transaction.transaction_type,
        )

        analysis["overall_risk_score"] = overall_risk

        # Determine decision based on risk score and critical factors
        decision = self._determine_decision(
            overall_risk,
            analysis,
            network,
            treasury,
            validators,
        )

        analysis["decision"] = decision.value
        analysis["reasoning"] = self._generate_reasoning(analysis, decision)

        # Log the decision
        self.decision_log.append(analysis)
        self.analysis_history.append(analysis)

        return decision, analysis

    # ============================================
    # FRAUD RISK CALCULATION
    # ============================================

    def _calculate_fraud_risk(self, transaction: TransactionMetrics) -> float:
        """
        Detect potential fraud based on:
        - User history and behavior patterns
        - New IP address or unusual location
        - Wallet age (new wallets = higher risk)
        - Transaction patterns (velocity, amounts)
        """
        risk = 0.0

        # User history score (inverse relationship)
        # Low history score = higher fraud risk
        user_score_factor = (100 - transaction.user_history_score) * 0.3
        risk += user_score_factor

        # New IP detection
        if transaction.ip_new:
            risk += 20

        # Wallet age analysis
        if transaction.wallet_age_days < 7:
            risk += 25
        elif transaction.wallet_age_days < 30:
            risk += 15
        elif transaction.wallet_age_days < 90:
            risk += 5

        # Transaction velocity
        if transaction.previous_transactions == 0:
            risk += 15  # First time user
        elif transaction.previous_transactions < 5:
            risk += 10  # Few transactions

        # Cap at 100
        return min(risk, 100.0)

    # ============================================
    # NETWORK CONGESTION RISK
    # ============================================

    def _calculate_congestion_risk(self, network: NetworkMetrics) -> float:
        """
        Monitor network congestion and capacity
        - Pending transaction backlog
        - Block capacity utilization
        - Gas prices and block times
        """
        if network.max_block_capacity == 0:
            return 50.0

        congestion_percent = (network.pending_transactions / network.max_block_capacity) * 100
        
        if congestion_percent > CONGESTION_THRESHOLD_HIGH:
            risk = 75 + (min(congestion_percent - CONGESTION_THRESHOLD_HIGH, 25))
        elif congestion_percent > CONGESTION_THRESHOLD_LOW:
            risk = 50 * (congestion_percent / CONGESTION_THRESHOLD_HIGH)
        else:
            risk = 25 * (congestion_percent / CONGESTION_THRESHOLD_LOW)

        # Gas price factor
        normalized_gas = min(network.average_gas_price / 1000, 1.0)
        risk += normalized_gas * 15

        # Block time degradation
        if network.block_time_seconds > 15:
            risk += 20

        return min(risk, 100.0)

    # ============================================
    # TREASURY HEALTH RISK
    # ============================================

    def _calculate_treasury_risk(self, treasury: TreasuryMetrics) -> float:
        """
        Assess treasury health and sustainability
        - Reserve ratio (balance / burn rate)
        - Inflow vs. outflow balance
        - Runway projection
        """
        if treasury.required_minimum == 0:
            return 25.0

        health_ratio = (treasury.total_balance / treasury.required_minimum) * 100

        if health_ratio < TREASURY_HEALTH_THRESHOLD_CRITICAL:
            risk = 90
        elif health_ratio < TREASURY_HEALTH_THRESHOLD_WARNING:
            risk = 60 * (TREASURY_HEALTH_THRESHOLD_WARNING / health_ratio)
        else:
            risk = 30 * (TREASURY_HEALTH_THRESHOLD_WARNING / health_ratio)

        # Burn rate analysis
        if treasury.reserve_ratio < 3:  # Less than 3 months runway
            risk += 25
        elif treasury.reserve_ratio < 6:
            risk += 15

        # Inflow/outflow imbalance
        if treasury.monthly_inflow > 0:
            burn_ratio = treasury.monthly_burn_rate / treasury.monthly_inflow
            if burn_ratio > 1.5:
                risk += 20

        return min(risk, 100.0)

    # ============================================
    # GOVERNANCE RISK
    # ============================================

    def _calculate_governance_risk(self, governance: GovernanceMetrics) -> float:
        """
        Assess governance health and participation
        - Voter participation rates
        - Proposal execution times
        - Active governance participation
        """
        risk = 0.0

        # Low participation = higher risk
        if governance.voter_participation_rate < 30:
            risk += 40
        elif governance.voter_participation_rate < 50:
            risk += 25
        elif governance.voter_participation_rate < 70:
            risk += 10
        else:
            risk += 5

        # High proposal velocity = governance stress
        if governance.proposal_count_7days > 50:
            risk += 30
        elif governance.proposal_count_7days > 20:
            risk += 15

        # Slow execution = governance inefficiency
        if governance.proposal_avg_execution_time_hours > 168:  # 1 week
            risk += 15

        # Low active participants
        if governance.active_governance_token_holders < 1000:
            risk += 20

        return min(risk, 100.0)

    # ============================================
    # VALIDATOR RISK
    # ============================================

    def _calculate_validator_risk(self, validators: ValidatorMetrics) -> float:
        """
        Assess validator network health
        - Average uptime and reliability
        - Validator count and decentralization
        - Slashing events
        """
        risk = 0.0

        # Low uptime = unreliable network
        if validators.average_uptime < VALIDATOR_UPTIME_THRESHOLD:
            risk += 50 * ((VALIDATOR_UPTIME_THRESHOLD - validators.average_uptime) / VALIDATOR_UPTIME_THRESHOLD)

        # Insufficient validator count
        if validators.validator_count < 10:
            risk += 40
        elif validators.validator_count < 21:
            risk += 20

        # High concentration = centralization risk
        if validators.max_stake_concentration > STAKING_CONCENTRATION_THRESHOLD:
            risk += 35
        elif validators.max_stake_concentration > 25:
            risk += 15

        # Slashing incidents
        risk += validators.slashing_incidents_7days * 10

        # High commission rates
        if validators.avg_commission_rate > 15:
            risk += 15

        return min(risk, 100.0)

    # ============================================
    # STAKING RISK
    # ============================================

    def _calculate_staking_risk(self, staking: StakingMetrics) -> float:
        """
        Monitor staking health and activity
        - Staking ratio and participation
        - Concentration risks
        - Unstaking pressure
        """
        risk = 0.0

        # Low staking participation
        if staking.staking_ratio < 30:
            risk += 40
        elif staking.staking_ratio < 50:
            risk += 20
        elif staking.staking_ratio < 70:
            risk += 5

        # High concentration
        if staking.top_validator_concentration > 40:
            risk += 35
        elif staking.top_validator_concentration > 25:
            risk += 15

        # High unstaking requests = liquidity stress
        if staking.daily_unstaking_requests > 1000:
            risk += 30
        elif staking.daily_unstaking_requests > 500:
            risk += 15

        # Low average delegation = weak incentives
        if staking.avg_delegation_size < 100:
            risk += 15

        return min(risk, 100.0)

    # ============================================
    # LIQUIDITY RISK
    # ============================================

    def _calculate_liquidity_risk(self, liquidity: LiquidityMetrics) -> float:
        """
        Assess market liquidity and trading health
        - DEX volume and depth
        - Bid-ask spreads
        - Slippage analysis
        """
        risk = 0.0

        # Low trading volume
        if liquidity.dex_volume_24h < liquidity.min_liquidity_threshold * 0.5:
            risk += 50
        elif liquidity.dex_volume_24h < liquidity.min_liquidity_threshold:
            risk += 30

        # Wide bid-ask spreads
        if liquidity.bid_ask_spread > 2.0:
            risk += 35
        elif liquidity.bid_ask_spread > 1.0:
            risk += 20
        elif liquidity.bid_ask_spread > 0.5:
            risk += 10

        # High slippage
        if liquidity.slippage_1m_trade > 5.0:
            risk += 30
        elif liquidity.slippage_1m_trade > 2.0:
            risk += 15

        # Low LP count
        if liquidity.liquidity_provider_count < 50:
            risk += 25

        return min(risk, 100.0)

    # ============================================
    # OVERALL RISK CALCULATION
    # ============================================

    def _calculate_overall_risk(
        self,
        fraud_risk: float,
        congestion_risk: float,
        treasury_risk: float,
        governance_risk: float,
        validator_risk: float,
        staking_risk: float,
        liquidity_risk: float,
        transaction_type: str,
    ) -> float:
        """
        Calculate weighted overall risk based on transaction type
        Different transaction types have different risk weightings
        """

        weights = self._get_transaction_weights(transaction_type)

        overall_risk = (
            fraud_risk * weights["fraud"] +
            congestion_risk * weights["congestion"] +
            treasury_risk * weights["treasury"] +
            governance_risk * weights["governance"] +
            validator_risk * weights["validator"] +
            staking_risk * weights["staking"] +
            liquidity_risk * weights["liquidity"]
        )

        # Cap at 100
        return min(overall_risk, 100.0)

    def _get_transaction_weights(self, transaction_type: str) -> Dict[str, float]:
        """
        Get risk weighting factors based on transaction type
        Weights sum to 1.0
        """

        default_weights = {
            "fraud": 0.25,
            "congestion": 0.15,
            "treasury": 0.15,
            "governance": 0.10,
            "validator": 0.12,
            "staking": 0.10,
            "liquidity": 0.13,
        }

        type_specific_weights = {
            "payment": {"fraud": 0.35, "congestion": 0.20, "liquidity": 0.20},
            "token_creation": {"treasury": 0.30, "governance": 0.20, "fraud": 0.20},
            "contract_deployment": {"validator": 0.25, "governance": 0.20, "fraud": 0.20},
            "blockchain_creation": {"validator": 0.30, "treasury": 0.25, "governance": 0.20},
            "governance": {"governance": 0.40, "staking": 0.25, "validator": 0.15},
            "staking": {"staking": 0.40, "validator": 0.25, "liquidity": 0.20},
            "trading": {"liquidity": 0.40, "fraud": 0.30, "congestion": 0.20},
        }

        if transaction_type in type_specific_weights:
            weights = default_weights.copy()
            weights.update(type_specific_weights[transaction_type])
            # Normalize to sum to 1.0
            total = sum(weights.values())
            return {k: v / total for k, v in weights.items()}

        return default_weights

    # ============================================
    # DECISION LOGIC
    # ============================================

    def _determine_decision(
        self,
        overall_risk: float,
        analysis: Dict,
        network: NetworkMetrics,
        treasury: TreasuryMetrics,
        validators: ValidatorMetrics,
    ) -> Decision:
        """
        Determine approval decision based on risk score and critical conditions
        """

        # Critical conditions that trigger escalation
        if self._has_critical_conditions(network, treasury, validators):
            return Decision.ESCALATE

        # Decision thresholds
        if overall_risk < 25:
            return Decision.APPROVE
        elif overall_risk < 50:
            return Decision.REVIEW
        elif overall_risk < 75:
            return Decision.REVIEW
        else:
            return Decision.REJECT

    def _has_critical_conditions(
        self,
        network: NetworkMetrics,
        treasury: TreasuryMetrics,
        validators: ValidatorMetrics,
    ) -> bool:
        """Check for critical platform conditions requiring escalation"""

        # Network emergency
        if network.pending_transactions > network.max_block_capacity * 2:
            return True

        # Treasury emergency
        if treasury.total_balance < treasury.required_minimum * 0.2:
            return True

        # Validator network failure
        if validators.average_uptime < 80:
            return True

        return False

    # ============================================
    # REPORTING & EXPLANATIONS
    # ============================================

    def _generate_reasoning(self, analysis: Dict, decision: Decision) -> str:
        """Generate human-readable reasoning for the decision"""

        reasoning = f"Decision: {decision.value.upper()}\n"
        reasoning += f"Overall Risk Score: {analysis['overall_risk_score']:.1f}/100\n\n"

        reasoning += "Risk Breakdown:\n"
        for metric, score in analysis["metrics"].items():
            reasoning += f"  - {metric.replace('_', ' ').title()}: {score:.1f}\n"

        if decision == Decision.APPROVE:
            reasoning += "\n✅ All metrics within acceptable thresholds. Auto-approved."
        elif decision == Decision.REVIEW:
            reasoning += "\n🔍 Mixed metrics detected. Flagged for manual review."
        elif decision == Decision.REJECT:
            reasoning += "\n❌ High-risk conditions detected. Auto-rejected."
        elif decision == Decision.ESCALATE:
            reasoning += "\n⚠️  Critical platform conditions. Escalated to security team."

        return reasoning

    def get_decision_history(self, limit: int = 100) -> List[Dict]:
        """Get recent decision history"""
        return self.decision_log[-limit:]

    def get_risk_summary(self) -> Dict:
        """Get summary statistics of recent decisions"""
        if not self.decision_log:
            return {}

        recent = self.decision_log[-100:]
        decisions = [d["decision"] for d in recent]
        
        return {
            "total_analyzed": len(recent),
            "approved": decisions.count("approve"),
            "rejected": decisions.count("reject"),
            "review": decisions.count("review"),
            "escalated": decisions.count("escalate"),
            "average_risk": sum(d["overall_risk_score"] for d in recent) / len(recent),
            "approval_rate": decisions.count("approve") / len(recent) * 100,
        }


# ============================================
# EXAMPLE USAGE
# ============================================

if __name__ == "__main__":
    # Initialize the algorithm
    algorithm = NovaCorAlgorithm()

    # Create sample metrics
    transaction = TransactionMetrics(
        transaction_id="tx_123456",
        transaction_type="token_creation",
        amount=1000.0,
        user_history_score=75.0,
        ip_new=False,
        wallet_age_days=180,
        previous_transactions=42,
        timestamp=datetime.now(),
    )

    network = NetworkMetrics(
        pending_transactions=500,
        max_block_capacity=2000,
        average_gas_price=50.0,
        block_time_seconds=12.0,
        network_participants=15000,
        active_validators=21,
    )

    treasury = TreasuryMetrics(
        total_balance=50000000.0,
        required_minimum=25000000.0,
        monthly_burn_rate=1000000.0,
        monthly_inflow=2000000.0,
        reserve_ratio=50.0,
    )

    governance = GovernanceMetrics(
        proposal_count_7days=15,
        voter_participation_rate=65.0,
        proposal_avg_execution_time_hours=48.0,
        active_governance_token_holders=5000,
    )

    validators = ValidatorMetrics(
        validator_count=21,
        average_uptime=98.5,
        max_stake_concentration=12.0,
        slashing_incidents_7days=0,
        avg_commission_rate=5.0,
    )

    staking = StakingMetrics(
        total_staked=600000000.0,
        staking_ratio=60.0,
        daily_unstaking_requests=100,
        top_validator_concentration=12.0,
        avg_delegation_size=5000.0,
    )

    liquidity = LiquidityMetrics(
        dex_volume_24h=50000000.0,
        bid_ask_spread=0.15,
        slippage_1m_trade=0.5,
        liquidity_provider_count=500,
        min_liquidity_threshold=10000000.0,
    )

    # Run analysis
    decision, analysis = algorithm.analyze_and_decide(
        transaction, network, treasury, governance, validators, staking, liquidity
    )

    print("=" * 60)
    print("NOVA CORE ALGORITHM - DECISION ANALYSIS")
    print("=" * 60)
    print(analysis["reasoning"])
    print("=" * 60)
    print("SUMMARY:")
    print(algorithm.get_risk_summary())
