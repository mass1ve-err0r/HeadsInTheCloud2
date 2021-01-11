from pygments import highlight
from pygments.lexers.objective import ObjectiveCLexer, LogosLexer
from pygments.formatters.html import HtmlFormatter
from pygments.styles.xcode import XcodeStyle
from os import walk, path
from os.path import splitext
from pathlib import Path
from time import sleep
import subprocess

targetSDK = "SDK12"  # change as needed
targetType = "public"  # public, private, dylib or protocols
sourceDir = "Frameworks"  # Frameworks, PrivateFramworks, lib, protocols
FrameworksDir = f"./static/cdn/{targetSDK}/Frameworks"
PrivateFrameworksDir = f"./static/cdn/{targetSDK}/PrivateFrameworks"
ProtoDir = f"./static/cdn/{targetSDK}/protocols"
LibsDir = f"./static/cdn/{targetSDK}/lib"
targetDir = f"./static/cdn/headers/{targetSDK}/Frameworks"
# <editor-fold desc="HTML WRAPS / EDIT THE IOS VERSION HERE">
html_start = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>$&@filename | HITC2</title>
        
        <!-- SEO Things (Basic) -->
        <meta name="description" content="Your iOS Header Service">
        <meta name="keywords" content="ios headers, headers, ios, reverse engineering, ios re, ios jailbreak, jailbreaking, headers, heads in the cloud">
        <meta name="author" content="Saadat Baig">
        <meta name="copyright" content="2019-2021 Saadat Baig">
        <meta name="robots" content="index,nofollow">

        <!-- SEO Things (OpenGraph) -->
        <meta property="og:name" content="HeadsInTheCloud2">
        <meta property="og:description" content="Your iOS Header Servic">
        <meta property="og:locale" content="en_US">
        <meta property="og:locale:alternate" content="de_DE">
        <meta property="og:site_name" content="HeadsInTheCloud2">
        <meta property="og:url" content="https://headers.saadat.dev/">

        <!-- SEO Things (Twitter + Others) -->
        <meta name="twitter:creator" content="saadat603">

        <!-- Google Fonts -->
        <link rel="preconnect" href="https://fonts.gstatic.com">
        <link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">

        <!-- Bootstrap 5.0 CSS -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-giJF6kkoqNQ00vy+HMDP7azOuL0xtbfIcaT9wjKHr8RbDVddVHyTfAAsrekwKmP1" crossorigin="anonymous">
        
        <!-- custom CSS -->
        <link rel="stylesheet" href="/static/css/header_view.css">
    </head>
    <body class="min-vh-100">
        <!-- Navbar -->
        <nav class="navbar navbar-dark top">
            <div class="container">
                <a href="/" class="navbar-brand mx-auto" style="font-size: 20px; font-weight: bold">
                    HeadsInTheCloud 2
                </a>
            </div>
        </nav>
        <nav class="top pb-3" aria-label="breadcrumb" style="top: 56px; width: 100%; --bs-breadcrumb-divider: '>';">
            <div class="container">
                <ol class="breadcrumb text-white p-1">
                    <li class="breadcrumb-item"><a class="anothergray" href="/">Home</a></li>
                    <li class="breadcrumb-item"><a class="anothergray" href="/sdks">SDKs</a></li>
                    <li class="breadcrumb-item"><a class="anothergray" href="/sdks/12">12.1.2</a></li>
                    <li class="breadcrumb-item"><a class="anothergray" href="/sdks/12/$&@framework?type=$&@type">$&@framework</a></li>
                    <li class="breadcrumb-item" aria-current="page">$&@filename</li>
                </ol>
            </div>
        </nav>
        <!-- Header Content -->
        <div class="container">
            <div class="row pb-5">
                <h2 class="text-white pb-1">Standard Header</h2>
                <div class="col">
"""
html_section2 = """
                </div>
            </div>
            <div class="row">
                <h2 class="text-white pb-1">Logified Header</h2>
                <div class="col">
"""
html_end = """
                </div>
            </div>
        </div>
        <!-- Footer -->
        <div class="footer mt-auto">
            <div class="container-fluid">
                <div class="container">
                    <hr class="text-white">
                    <div class="row">
                        <div class="col text-center p-1">
                            <div id="contactTwitter">
                                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-brand-twitter" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="#00abfb" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M22 4.01c-1 .49 -1.98 .689 -3 .99c-1.121 -1.265 -2.783 -1.335 -4.38 -.737s-2.643 2.06 -2.62 3.737v1c-3.245 .083 -6.135 -1.395 -8 -4c0 0 -4.182 7.433 4 11c-1.872 1.247 -3.739 2.088 -6 2c3.308 1.803 6.913 2.423 10.034 1.517c3.58 -1.04 6.522 -3.723 7.651 -7.742a13.84 13.84 0 0 0 .497 -3.753c-.002 -.249 1.51 -2.772 1.818 -4.013z" />
                                </svg>
                                <a class="small" href="https://twitter.com/saadat603" target="_blank">@saadat603</a>
                            </div>
                        </div>
                        <div class="col text-center p-1">
                            <div id="viewOnGitHub">
                                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-brand-github" width="24" height="24" viewBox="0 0 24 24" stroke-width="1.5" stroke="#00abfb" fill="none" stroke-linecap="round" stroke-linejoin="round">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
                                    <path d="M9 19c-4.3 1.4 -4.3 -2.5 -6 -3m12 5v-3.5c0 -1 .1 -1.4 -.5 -2c2.8 -.3 5.5 -1.4 5.5 -6a4.6 4.6 0 0 0 -1.3 -3.2a4.2 4.2 0 0 0 -.1 -3.2s-1.1 -.3 -3.5 1.3a12.3 12.3 0 0 0 -6.2 0c-2.4 -1.6 -3.5 -1.3 -3.5 -1.3a4.2 4.2 0 0 0 -.1 3.2a4.6 4.6 0 0 0 -1.3 3.2c0 4.6 2.7 5.7 5.5 6c-.6 .6 -.6 1.2 -.5 2v3.5" />
                                </svg>
                                <a class="small" href="https://github.com/mass1ve-err0r/HeadsInTheCloud2" target="_blank">View on GitHub</a>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm text-center p-1">
                            <small class="text-muted">Special thanks to SparkDev et al. for providing SDK dumps.<br>
                                Without these beautiful people this service would not exist!
                            </small>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm text-center p-3">
                            <small class="text-muted">© 2020-2021 Saadat Baig<br>Made with ❤️ in Germany</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-ygbV9kiqUc6oa4msXn9868pTtWMgiQaeYH7/t7LECLbyPA2x65Kgf80OJFdroafW" crossorigin="anonymous"></script>
    </body>
</html>
"""
# </editor-fold>


if __name__ == '__main__':
    print("SDK scanner & converter --- iOS 12")
    for root, subdirs, fyles in walk(FrameworksDir): #  <-- swap this dir out as needed
        print(f"=== working in: {root}")
        _dirname = root[root.rindex('/')+1:]
        subdirs.sort()
        for subdir in subdirs:
            # print(f"--> Subdirectory: {subdir}")
            print(f"{subdir}")
            Path(f"{targetDir}/{subdir}").mkdir(parents=True, exist_ok=True)
        fyles.sort()
        for filename in fyles:
            if filename == ".DS_Store":
                print("Found .DS_Store, ignoring...")
                continue
            if splitext(filename)[1] == ".framework":
                print("Found empty frmaework, ignoring...")
                continue
            file_path = path.join(root, filename)
            target_file_path = f"{targetDir}/{_dirname}/{filename}.html"
            # print(f"--> Processing File {filename}")
            with open(file_path, 'r+') as header:
                with open(target_file_path, 'a+') as header_html:
                    # header prepping
                    header_content = header.read()
                    html_start_preformatted = html_start.replace("$&@filename", f"{filename}").replace("$&@framework", f"{_dirname}").replace("$&@type", f"{targetType}")

                    # logify
                    header_logified_raw = subprocess.Popen([ "/Users/saadat/theos/bin/logify.pl", f"./static/cdn/{targetSDK}/{sourceDir}/{_dirname}/{filename}" ],
                                                           stdout=subprocess.PIPE)
                    header_logified_bytes = header_logified_raw.stdout.read()
                    header_logified_parsed = header_logified_bytes.decode('utf-8')[ :-1 ]
                    header_logified_corrected = header_logified_parsed.replace("{ ", "{\n    ").replace("; ", ";\n    ").replace("\n    }", "\n}")

                    # lexing
                    header_formatted = highlight(header_content, ObjectiveCLexer(), HtmlFormatter(style=XcodeStyle))
                    header_logified = highlight(header_logified_corrected, LogosLexer(), HtmlFormatter(style=XcodeStyle))

                    # out
                    complete_header_formatted = f"{html_start_preformatted + header_formatted +html_section2 + header_logified + html_end}"
                    header_html.write(complete_header_formatted)
            # print("End of File Processing.")
            sleep(0.07)
        # input("press enter to start next iteration")
    print("DONE")
