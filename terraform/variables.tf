variable "project_id" {
  description = "The GCP project ID"
  type        = string
}


variable "gcp_svc_key" {
    description = "The path to the GCP service account key file"
    type        = string
}

variable "region" {
  description = "The region of Project"
  type = string
}
