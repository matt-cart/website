title: How I built this website (Part 4)
date: 2018-07-14
tags: aws, flask, web development
summary: In this post we will configure an Amazon Web Services EC2 instance to host our website.

## Introduction

This series is a step-by-step tutorial for making a website like the one you're currently browsing. It includes an introduction to the Flask web framework, an introduction to Markdown (the markup language used to write this post), and also an introduction to hosting websites using Amazon Web Services.

Posts in this series:
1. [Flask](/blog/how-i-built-this-website-(part-1\))
2. [Introduction to Markdown](/blog/how-i-built-this-website-(part-2\))
3. [Configuring the Markdown blog](/blog/how-i-built-this-website-(part-4\))
4. Amazon Web Services (you are here)


asdfsafsaf


## Getting started

If you don't already have an account with Amazon Web Services, go ahead and create one now. AWS provides a substantial set of services that fall under their "free tier" for the first year that you have your account.

After creating your account, register the domain you want to use for your website. This can be done using Amazon's [Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html) service. If you already own a domain name, you can [transfer it to Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-transfer-to-route-53.html?console_help=true).

## Configuring Route 53

Once you have a domain name registered with AWS a "[hosted zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html)" will automatically be created. Hosted zones are containers for "records". Records indicate how traffic should be routed for your domain. After registering your domain with AWS, you should see one hosted zone for your domain. It should contain two records. One record is of type "NS" (name server) and the other should be of type "SOA" (start of authority). After we configure our EC2 instance we'll circle back to this hosted zone and create two custom records that route internet traffic to our EC2 instance.

## Setting up an Amazon EC2 instance

Amazon EC2 instances are virtual servers in the cloud. Before launching an EC2 instance, go through Amazon's documentation for [getting set up with EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html). Once you're ready, navigate to the EC2 servince in the AWS console and click "Launch Instance". 



### Reserving an Elastic IP

### Linking your instance with your registered domain


## Setting up your website

### Installing packages

### WSGI and Apache

## Overview of AWS online resources

* [Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)

## Costs