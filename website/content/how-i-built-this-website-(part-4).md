title: How I built this website (Part 4)
date: 2018-07-14
tags: aws, flask, web development
summary: In this post we will configure an Amazon Web Services EC2 instance to host our website.

## Introduction

This series is a step-by-step tutorial for making a website like the one you're currently browsing. It includes an introduction to the Flask web framework, an introduction to Markdown (the markup language used to write this post), and also an introduction to hosting and deploying websites using Amazon Web Services.

Posts in this series:
1. [Introduction to Flask](</blog/how-i-built-this-website-(part-1)>)
2. [Introduction to Markdown](</blog/how-i-built-this-website-(part-2)>)
3. [Configuring a Markdown blog](</blog/how-i-built-this-website-(part-3)>)
4. Deploying to Amazon Web Services (you are here)

In this post we'll cover the deployment of our fully functional website to Amazon Web Services (AWS). To accomplish this we will spin up a virtual server using Amazon EC2 to host our website and then use Amazon's Route 53 to direct internet traffic from our domain of choice to our hosted web server. This setup as I've devised it is very DIY. There are hosting services that are far more direct (Amazon Lightsail is one such example). That said, building things from scratch tends to be pedagogically more valuable. This setup also affords complete control over configuration, something that is sacrificed with other services that handle the configuration for you.

<img class="center-image" width="45%" src="/static/img/aws_logo.svg" />

* * * 

## Before starting

To follow this post, you'll need to [create an account with Amazon Web Services](https://portal.aws.amazon.com/billing/signup#/start). This is free to do. Additionally, Amazon provides many services that we are about to discuss for free in the first year of membership (I discuss costs of hosting in the Appendix of this post). You will also need a registered domain name. Mine, for example, is "mattcarter.co". For the purposes of demonstration, I purchased a new domain "mattcarter.info" in which I'll re-deploy this website. If you already own a domain and it is not registered with Amazon, you'll need to transfer it to Amazon's ownership. If you don't already own one, we'll cover the registration process below.

## Overview

The procedure we will follow in this post will proceed as follows:
1. Create an EC2 instance
	* This will be done in AWS's EC2 web interface. 
2. Configure EC2 instance
	* This includes installing new software on the native OS, such as the Apache2 web server.
3. Setup website repository
	* Clone from GitHub and install necessary environment.
4. Direct traffic from your registered domain to your hosted website.
	* This will be done in AWS's Route 53 interface.

## A note on the final Flask project

Up to this point, we've discussed our Flask project in the context of using our development server to test the functionality and aesthetics of our nascent website. Now that we are going to deploy our website to a "real" web server, I should note two additional files that I have not previously discussed: `website.wsgi` and `setup.sh`:
* `website.wsgi` is necessary for getting our web application to talk to our web server, we'll discuss that later. 
* `setup.sh` is a means by which we can semi-automate the configuration of our Ubuntu server environment. Some of the tools we need to use are a little finicky with regards to dependencies and this script should make the process go a little smoother.

* * *

## Setting your Amazon EC2 instance

### The EC2 console

From the AWS home page, navigate to the EC2 console via the "Services" dropdown. You should land in the "Instances" panel; click "Launch Instance". From the list of AMI's, select the "Ubuntu Server 16.04 LTS (HVM)" option[^1]. In the next page, you will be asked to select an instance type. Choose "t2.micro"; it is free-tier eligible and also the instance type this is used to host this very website. For a simple static blog like this with a low volume of expected traffic this will work great. If you think you want to go bigger, see this [AWS blog post](https://aws.amazon.com/ec2/instance-types/) for more information. When you've selected the instance type you want, go ahead and click "Review and Launch". 

After reviewing your instance setup and clicking "Launch" you will be prompted to create a new key pair. Name the key pair something memorable and download it. As the pop-up states: **Store the key pair file in a secure and accessible location**. You will need this to log in to your instance and will not have another opportunity to download it.

Now your instance is spinning up. The next step is to update the instance's "[security group](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-network-security.html?icmpid=docs_ec2_console)" in order to allow inbound traffic from the outside world. To do this, click on your instance in the Instance panel and look in the "Description" at the bottom of the page for the "Security groups" field. Your security group name, by default, will be something like "launch-wizard-1" and it will be a link. Click this link to go to the Security Groups panel. Click on the security group and select "Edit inbound rules" from the "Actions" dropdown. Add a new rule and select "HTTP" from the "Type" dropdown and then select "Anywhere" in the "Source" dropdown. Add another new rule and select "HTTPS" from the "Type" dropdown and then select "Anywhere" in the "Source" dropdown. Save these inbound rules. Your inbound rules should now look something like this:

<img class="center-image" width="85%" src="/static/img/inbound_rules.png" />

Now your soon-to-be-deployed website will be visible to the outside world. Without adding these inbound rules the default security group's firewall would have closed off all access.

The next step is to navigate to the "Elastic IPs" panel (the link is in the "Network and Security" section of the left-hand menu). We are going to create an [Elastic IP address](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html?icmpid=docs_ec2_console) for our instance. This will reserve a static IP that we can always access for our website[^2]. In the Elastic IP panel, select "Allocate new address" and follow the prompt. Then, select the new address and click "Associate address" under the now-familiar "Actions" dropdown. On the next page, select your instance via its instance ID under the "Instance" dropdown and click "Associate".

Navigate back to the Instances panel and click on your instance with its newly associated Elastic IP. In the description section you'll see a field for "Public DNS (IPv4)". Copy the URL next to it to your clipboard. For reference, the URL I am copying is `ec2-18-217-98-123.us-east-2.compute.amazonaws.com`.


### Remote accessing your instance

To log in to your instance we will leverage the key pair file that we downloaded previously. Navigate to the directory where the file lives and modify its permissions with the following command:
```
chmod 400 /path/KEYNAME.pem
```
This is an extra precaution against allowing others access to this file (and therefore denying them remote access to your instance).

Login to your instance with the following command:

```
ssh -i "[name-of-key]" ubuntu@[public-dns-ipv4]
```
Here, replace `[name-of-key]` with the actual name of your private key, including *.pem* the extension. Also replace `[public-dns-ipv4]` with the "Public DNS (IPv4)" snippet you copied from above. Now you should be logged in to your EC2 instance. 

Clone the git repository containing your Flask project into your home folder. Navigate into the website directory and run the `setup.sh` script. You will see a lot of text on the screen and periodically be prompted with questions, answer yes to all of them. 

Assuming the setup script completed without errors, let's finish the setup process by creating our Python virtual environment:

```posh
ubuntu@amazonaws$ virtualenv venv
ubuntu@amazonaws$ . venv/bin/activate
ubuntu@amazonaws$ pip install -r requirements.txt
```

One of the steps taken in the `setup.sh` script was to install the Apache2 web server. You can check that your instance is properly configured by entering your Elastic IP into the address bar of your browser. You should see the Apache2 default page!

<img class="center-image" width="70%" src="/static/img/apache2_default.png" />

Apache2, by default, contains boilerplate HTML that gets served when you access the `/` route for your domain. We'll rectify this by pointing the `/` domain to our web app. To do this, we have to edit one of the main Apache2 configuration files found at `/etc/apache2/sites-enabled/000-default.conf`. To start, it will look like this:

```posh
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
</VirtualHost>
```

Go ahead and update this file so that in the end it looks like this:

```posh
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        #ServerName www.example.com

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        WSGIDaemonProcess website threads=5
        WSGIScriptAlias / /var/www/html/website/website.wsgi

        <Directory website>
                WSGIProcessGroup website
                WSGIApplicationGroup %{GLOBAL}
                Order deny,allow
                Allow from all
        </Directory>

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
</VirtualHost>
```

The key bit is the snippet `WSGIScriptAlias / /var/www/html/website/website.wsgi` which points the `/` domain to the `website.wsgi` file in our web application. Astute readers will notice that our web application exists in `/home/ubuntu/website` not `/var/www/html/website`. This was taken care of by our `setup.sh` which created a soft-link between the `website` directory in our home folder to the `/var/www/html` folder.

Restart Apache with:

```posh
sudo /etc/init.d/apache2 restart
```

And then refresh your browser window with our instance's IP. You should see your fully functional website. The next and final step is getting our website to appear when we enter our actual domain name into a browser's address bar. 

## Routing traffic through your registered domain

If you haven't already registered a domain through Amazon Route 53, go ahead and do that now. Most common top-level domains cost $12/year or less. After you've purchased your domain it will eventually show up in the "Registered domains" tab of the Route 53 console. (If you need to transfer your domain to Route 53 from a different hosting servies, see [these help docs](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-transfer-to-route-53.html?console_help=true)).

The next step is to update the "[hosted zone](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html)" for your domain. Hosted zones are containers for "records". Records indicate how traffic should be routed for your domain. After the registration of your domain with AWS is complete (it may take about 10 minutes), you should automatically see a hosted zone for your domain. It will contain two records: one record is of type "NS" (name server) and the other should be of type "SOA" (start of authority). We'd like to create two new "A" records that route traffic to our domain to our EC2 instance. For this part, you'll need the Elastic IP of your EC2 instance handy.

To create the first new record, click "Create Record Set". Leave the "Name" field blank and leave the "Type" field as-is. Paste the Elastic IP of your EC2 instance into the "Value" field and click "Create". Repeat this process, except this time, update the "Name" field with "www". Your list of record sets should now look something like this[^3]:

<img class="center-image" width="80%" src="/static/img/record_sets.png" />

These changes should propagate through Amazon's backend rather quickly. Within a minute or two you should be able to type your domain name into the address bar of your browser and your website will appear!


## Wrapping up

This concludes our tutorial. Along the way, we learned how to use Flask, Markdown and Amazon Web Services. I hope you found it interesting and helpful. If you have any questions or comments, please feel free to <a href="mailto:&#109;&#097;&#116;&#116;&#104;&#101;&#119;&#109;&#099;&#097;&#114;&#116;&#101;&#114;&#050;&#064;&#103;&#109;&#097;&#105;&#108;&#046;&#099;&#111;&#109;" target="_blank">reach out to me</a>.

Further links and resources can be found in the Appendix below.

* * * 

## Appendix

### Overview of AWS online resources

* [EC2 overview](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
	* [Setting up with EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html)
	* [Launching and connecting to instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html)
	* [Elastic IP addresses](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html?icmpid=docs_ec2_console)
	* [Network and security](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_Network_and_Security.html)
	* [Connecting to your instance with SSH](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)
	* [EC2 best practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
* [Route 53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)
	* [Hosted zones](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html)
	* [Routing traffic to an EC2 instance](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-ec2-instance.html)

### Other online resoures that helped me construct this blog

"[Running a Flask app on AWS EC2](https://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/)" by Frank Cleary at [Data Science Bytes](https://www.datasciencebytes.com/)

"[How to make a Flask blog in one hour or less](http://charlesleifer.com/blog/how-to-make-a-flask-blog-in-one-hour-or-less/)" by Charles Leifer at [charlesleifer.com](http://charlesleifer.com/)

"[Build a Simple, Static, Markdown-Powered Blog with Flask](http://www.jamesharding.ca/posts/simple-static-markdown-blog-in-flask/)" by James Harding at [jamesharding.ca](http://www.jamesharding.ca/)

"[The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)" by Miguel Grinberg at [blog.miguelgrinberg.com](https://blog.miguelgrinberg.com/index)

### Costs of using Amazon Web Services

As I noted at the top of this post, AWS provides a "free tier" of services for users in their first year of membership. This is an awesome perk to take advantage of. After the first year users will incur nominal costs for using the various services we've talked about in this post. Below I'll show what the various pricing models look like for maintaining a website like this one.

Two assumptions:
* I'm assuming you've registered a domain name with a common top-level domain like ".com". These usually cost around $12 but may deviate slightly from this. Note that when you pay for a domain you pay the cost for a year-long registration upfront, I've prorated this to a per-month cost in the tables below even though you will not be billed on a monthly basis.
* I'm also assuming that you chose the "t2.micro" instance size for your EC2 instance. Larger instances will incur larger costs.

General pricing models:
* *Route 53*: $0.50 per hosted zone per month.
* *EC2*: $0.0116 per hour of instance uptime (equates to $8.47 per month).

#### Costs during first year

<table class="table table-bordered">
	<thead>
		<tr>
			<th>Service</th>
			<th>Avg. monthly cost (<i>$</i>)</th>
			<th>Yearly cost (<i>$</i>)</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Domain registrar</td>
			<td>1.00</td>
			<td>12.00</td>
		</tr>
		<tr>
			<td>EC2</td>
			<td>0.00</td>
			<td>0.00</td>
		</tr>
		<tr>
			<td>Route 53</td>
			<td>0.50</td>
			<td>6.00</td>
		</tr>
		<tr>
			<td><b>TOTAL</b></td>
			<td>1.50</td>
			<td>18.00</td>
		</tr>
	</tbody>
</table>

#### Costs after first year

<table class="table table-bordered">
	<thead>
		<tr>
			<th>Service</th>
			<th>Avg. monthly cost (<i>$</i>)</th>
			<th>Yearly cost (<i>$</i>)</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Domain registrar</td>
			<td>1.00</td>
			<td>12.00</td>
		</tr>
		<tr>
			<td>EC2</td>
			<td>8.47</td>
			<td>101.64</td>
		</tr>
		<tr>
			<td>Route 53</td>
			<td>0.50</td>
			<td>6.00</td>
		</tr>
		<tr>
			<td><b>TOTAL</b></td>
			<td>9.97</td>
			<td>119.64</td>
		</tr>
	</tbody>
</table>

#### Costs with a reserved EC2 instance

The EC2 instances we've used up until this point have technically been "on-demand" instances that we treat as permanently available servers. Amazon allows one to purchase "reserved" instances at a heavily discounted price. You can reserve instances for 12 or 36 month terms. The catch is that you have to pay for the cost of these instances up-front. You can purchase reserved instances in the "Reserved Instances" panel of the EC2 console on the AWS website. There is a 36 month plan that costs $115 up front. This prorates to $38.33 per year and $3.19 per month for the duration of the reservation, cutting your EC2 costs by more than 60%. If you plan on keeping your website up for a span of several years, reserving an instance is a no brainer.[^4]

<table class="table table-bordered">
	<thead>
		<tr>
			<th>Service</th>
			<th>Avg. monthly cost (<i>$</i>)</th>
			<th>Yearly cost (<i>$</i>)</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Domain registrar</td>
			<td>1.00</td>
			<td>12.00</td>
		</tr>
		<tr>
			<td>EC2</td>
			<td>3.19</td>
			<td>38.33</td>
		</tr>
		<tr>
			<td>Route 53</td>
			<td>0.50</td>
			<td>6.00</td>
		</tr>
		<tr>
			<td><b>TOTAL</b></td>
			<td>4.69</td>
			<td>56.28</td>
		</tr>
	</tbody>
</table>

### Development workflow

Whenever I'm making changes to this site -- be it new blog posts, tweaking the CSS styling, etc. -- I always make the changes locally on my MacBook. I'll keep a Flask development server up and running as I'm making changes and periodically check to see what my updates look like in a live setting. Whenever I've finished a new feature or draft I'll commit the changes to my local Git repository. When I'm ready to make my changes I'll push them up to my GitHub repository. After that I'll log in to my EC2 instance and pull the changes down. I'll usually restart the Apache web server and then double check my changes. 

The important thing to note from this process is that I am never doing any development on my production server. Even if I discover a typo in a blog post after I've pushed it to production I will always go back to my development repository on my local machine and make the change there. The less you interact with your production machine, the better.

* * *

### Footnotes

[^1]: You could feasibly use any of these Linux distributions, I'm arbitrarily choosing Ubuntu. I haven't tested to see whether the rest of the tutorial applies if you choose a different distribution.
[^2]: Suppose our instance fails for some reason. When this happens, we want to minimize downtime. If we spin up a new instance to re-deploy our site, it will be assigned a random IP address. This means we would have to re-route or website traffic to a new IP address. These changes take time to propagate, resulting in more downtime than is needed. Elastic IP addresses are permanent and easily re-allocated to new instances. By assigning an Elastic IP address to our instance and routing website traffic to that IP address, we can be assured of never having to touch our DNS settings.
[^3]: I've registered a new dummy domain "mattcarter.info" for the sake of demonstration. My record sets for the domain "mattcarter.co" is essentially the same.
[^4]: It should be noted that reserved instances are not physical instances. Rather, they are billing conveniences. Say you have a running on-demand t2.micro instance that is incurring some hourly cost. You then purchase a reserved t2.micro instance for 12 months. This reservation automatically gets applied to the running t2.micro instance and the hourly costs cease (assuming you paid upfront for the entirety of the reservation. See [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html) for more information.
