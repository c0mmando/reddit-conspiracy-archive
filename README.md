# /r/Conspiracy Archive

This archive of the /r/conspiracy community on Reddit preserves 34,579 posts and 276,632 comments from August 15, 2008 through October 15, 2018.

---

## Repository Structure

Below is an overview of the repository structure for the Reddit conspiracy archive:

```
reddit-conspiracy-archive/
├── CNAME              # Custom domain file for GitHub Pages (optional)
├── conspiracy         # Contains the post pages and index files
├── favicon.ico        # Favicon for the archive site
├── illuminati.webp    # Associated image for the archive site
├── index.html         # Main landing page for the archive
├── README.md          # This README file
├── robots.txt         # Robots exclusion file
├── sitemaps           # Directory for generated sitemap files
├── static             # Directory containing static assets (CSS, JS, images)
└── user               # Directory for user-related files (if any)
```

Inside the `conspiracy` directory, the structure is as follows:

```
conspiracy/
├── comments         # Directory containing comment index files
├── index-comments   # Index files sorted by comments
├── index-date       # Index files sorted by date
├── index.html       # Main index page for /r/conspiracy posts
└── search.html      # Search page for the archive
```

> Note: Any HTML file that includes hard-coded SEO or meta tags may need updates if you plan to mirror or host the project differently.

---

## Download Options

You can either clone the repository or download the archive as a ZIP/TAR file:

### Clone via Git

```bash
git clone https://github.com/c0mmando/reddit-conspiracy-archive.git
```

### Download ZIP or TAR

1. **ZIP Download:**  
   Visit [https://github.com/c0mmando/reddit-conspiracy-archive](https://github.com/c0mmando/reddit-conspiracy-archive) and click the "Code" button. Then select "Download ZIP".

2. **TAR Download:**  
   Click the "Code" button and choose "Download TAR". GitHub provides these options automatically.

---

## Hosting via GitHub Pages

GitHub Pages is a straightforward way to host your static site online. Follow these steps to deploy your archive:

1. **Push Your Repository to GitHub**

   Make sure your repository is available on GitHub under your username. If you are starting fresh, run the following commands:

   ```bash
   git init
   git add .
   git commit -m "Initial commit of reddit-conspiracy-archive"
   git remote add origin https://github.com/c0mmando/reddit-conspiracy-archive.git
   git push -u origin main
   ```

2. **Configure GitHub Pages**

   - Open your repository on GitHub.
   - Go to **Settings**.
   - Scroll down to the **GitHub Pages** section.
   - Under **Source**, choose your branch (e.g., `main`) and select the folder (`/` if your `index.html` is at the root).
   - Click **Save**.
   - GitHub Pages will provide you with a URL where your site is hosted (e.g., `https://c0mmando.github.io/reddit-conspiracy-archive/`).

3. **Using a Custom Domain**

   If you want to use a custom domain:
   
   - Create a file named `CNAME` (with no file extension) in the repository root.
   - Add your custom domain (for example, `www.example.com`) on a single line.
   - Commit and push the file:

     ```bash
     git add CNAME
     git commit -m "Add CNAME for custom domain"
     git push
     ```

   - Update your DNS settings to point your domain to GitHub Pages. More details can be found in GitHub’s [custom domain guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

---

## Hosting via nginx

To host the archive on your own server with nginx, follow these steps:

1. **Install nginx**

   On Ubuntu/Debian:

   ```bash
   sudo apt update
   sudo apt install nginx
   ```

   On CentOS/RHEL:

   ```bash
   sudo yum install epel-release
   sudo yum install nginx
   ```

2. **Clone the Repository on Your Server**

   Clone the latest version into your desired web directory (e.g., `/var/www/html`):

   ```bash
   cd /var/www/html
   sudo git clone https://github.com/c0mmando/reddit-conspiracy-archive.git
   ```

3. **Configure nginx**

   Create a new configuration file (e.g., `/etc/nginx/sites-available/reddit-conspiracy-archive`):

   ```nginx
   server {
       listen 80;
       server_name your_domain_or_ip;

       root /var/www/html/reddit-conspiracy-archive;
       index index.html;

       location / {
           try_files $uri $uri/ =404;
       }
   }
   ```

   Replace `your_domain_or_ip` with your server’s domain name or IP address.

4. **Enable the Configuration**

   Enable the site by creating a symbolic link:

   ```bash
   sudo ln -s /etc/nginx/sites-available/reddit-conspiracy-archive /etc/nginx/sites-enabled/
   ```

5. **Restart nginx**

   Restart nginx to apply the changes:

   ```bash
   sudo systemctl restart nginx
   ```

6. **Access Your Site**

   Open your web browser and navigate to `http://your_domain_or_ip` to view the archive.

---

## Offline Viewing Instructions

To view the archive offline without a web server, you have two options:

### 1. File Explorer

- Navigate to the repository folder where you have cloned or downloaded the files.
- Open `index.html` with your preferred web browser.

### 2. Using a Local HTTP Server

For a more seamless offline navigation, you can use Python’s built-in server:

For Python 3:

```bash
cd /path/to/reddit-conspiracy-archive
python3 -m http.server 8000
```

For Python 2:

```bash
cd /path/to/reddit-conspiracy-archive
python -m SimpleHTTPServer 8000
```

Then open your browser and go to `http://localhost:8000/`.

---

## Additional Notes

- Ensure that the file permissions allow web servers like nginx (or your local HTTP server) to read the archive files.
- Any hard-coded SEO tags and meta elements within the HTML files should be reviewed and updated if you decide to mirror or rehost the archive.
- Changes on GitHub Pages might require a short time to take effect.
- Before hosting the archive publicly, please review any legal or privacy concerns related to its content.
