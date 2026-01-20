terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.16.0"
    }
  }
}

provider "google" {
  project = "project-f77e4ca1-f5aa-4470-bca"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "project-f77e4ca1-f5aa-4470-bca-demo-bucket"
  location      = "US"
  force_destroy = true

  uniform_bucket_level_access = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo" {
  dataset_id = "demo_dataset"
}