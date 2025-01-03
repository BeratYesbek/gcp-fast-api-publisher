provider "google" {
  project = var.project_id
  region  = var.region
    credentials = file(var.gcp_svc_key)
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.5"
    }
  }
}
