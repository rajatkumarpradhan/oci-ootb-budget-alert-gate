terraform {
  required_providers {
    oci = {
      source = "oracle/oci"
      version = "~> 7.0"
    }
  }
}
# Provider credentials must be configured by the operator. Never commit secrets.
variable "tenancy_ocid" { type = string }
variable "target_compartment_ocid" { type = string }
variable "recipients" {
  type = string
  description = "Delimited operator-approved alert email recipients"
}
variable "monthly_amount" {
  type = number
  default = 100
  validation {
    condition = var.monthly_amount > 0 && floor(var.monthly_amount) == var.monthly_amount
    error_message = "Use a positive whole-number budget in the rate-card currency."
  }
}
resource "oci_budget_budget" "monthly" {
  compartment_id = var.tenancy_ocid
  amount = var.monthly_amount
  reset_period = "MONTHLY"
  target_type = "COMPARTMENT"
  targets = [var.target_compartment_ocid]
  display_name = "monthly-cost-warning"
}
resource "oci_budget_alert_rule" "actual" {
  budget_id = oci_budget_budget.monthly.id
  threshold = 80
  threshold_type = "PERCENTAGE"
  type = "ACTUAL"
  recipients = var.recipients
  display_name = "actual-80-percent"
}
resource "oci_budget_alert_rule" "forecast" {
  budget_id = oci_budget_budget.monthly.id
  threshold = 100
  threshold_type = "PERCENTAGE"
  type = "FORECAST"
  recipients = var.recipients
  display_name = "forecast-100-percent"
}
