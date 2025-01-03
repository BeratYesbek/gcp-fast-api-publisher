resource "google_pubsub_topic" "pubsub_topic" {
  name = "users-read-data"
}

resource "google_pubsub_subscription" "subscription" {
  name  = "users-read-data-subscriber"
  topic = google_pubsub_topic.pubsub_topic.name
}

# Define the Protobuf schema
resource "google_pubsub_schema" "protobuf_schema" {
  name = "users-read-data-schema"

  type = "PROTOCOL_BUFFER"

  definition = <<PROTO
syntax = "proto3";

package com.example;

message User {
  string id = 1;
  string name = 2;
  string email = 3;
}
PROTO
}

resource "google_bigquery_dataset" "my_dataset" {
  dataset_id = "big_data_set"
  location   = "US"
}

resource "google_bigquery_table" "my_table" {
  table_id   = "users"
  dataset_id = google_bigquery_dataset.my_dataset.dataset_id

  schema = jsonencode([
    {
      name = "id"
      type = "STRING"
    },
    {
      name = "name"
      type = "STRING"
    },
    {
      name = "email"
      type = "STRING"
    }
  ])

}

