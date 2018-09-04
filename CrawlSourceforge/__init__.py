import re

hreflist=['<a itemprop="url" href="/projects/openofficeorg.mirror/?source=directory" title="Find out more about Apache OpenOffice"><h2>Apache OpenOffice</h2></a>',
 '<a itemprop="url" href="/projects/clonezilla/?source=directory" title="Find out more about Clonezilla"><h2>Clonezilla</h2></a>',
 '<a itemprop="url" href="/projects/hibernate/?source=directory" title="Find out more about Hibernate"><h2>Hibernate</h2></a>',
 '<a itemprop="url" href="/projects/eclipse-cs/?source=directory" title="Find out more about Eclipse Checkstyle Plug-in"><h2>Eclipse Checkstyle Plug-in</h2></a>',
 '<a itemprop="url" href="/projects/openproj/?source=directory" title="Find out more about OpenProj - Project Management"><h2>OpenProj - Project Management</h2></a>',
 '<a itemprop="url" href="/projects/moodle/?source=directory" title="Find out more about Moodle"><h2>Moodle</h2></a>',
 '<a itemprop="url" href="/projects/corefonts/?source=directory" title="Find out more about Microsoft\'s TrueType core fonts"><h2>Microsoft\'s TrueType core fonts</h2></a>',
 '<a itemprop="url" href="/projects/npppluginmgr/?source=directory" title="Find out more about Notepad++ Plugin Manager (old repo)"><h2>Notepad++ Plugin Manager (old repo)</h2></a>',
 '<a itemprop="url" href="/projects/sapnweclipse/?source=directory" title="Find out more about SAP NetWeaver Server Adapter for Eclipse"><h2>SAP NetWeaver Server Adapter for Eclipse</h2></a>',
 '<a itemprop="url" href="/projects/scrollout/?source=directory" title="Find out more about Scrollout F1"><h2>Scrollout F1</h2></a>',
 '<a itemprop="url" href="/projects/ubuntuzilla/?source=directory" title="Find out more about Ubuntuzilla: Mozilla Software Installer"><h2>Ubuntuzilla: Mozilla Software Installer</h2></a>',
 '<a itemprop="url" href="/projects/autoap/?source=directory" title="Find out more about AutoAP"><h2>AutoAP</h2></a>',
 '<a itemprop="url" href="/projects/assp/?source=directory" title="Find out more about Anti-Spam SMTP Proxy Server"><h2>Anti-Spam SMTP Proxy Server</h2></a>',
 '<a itemprop="url" href="/projects/amidst.mirror/?source=directory" title="Find out more about Amidst"><h2>Amidst</h2></a>',
 '<a itemprop="url" href="/projects/keepass/?source=directory" title="Find out more about KeePass"><h2>KeePass</h2></a>',
 '<a itemprop="url" href="/projects/codeblocks/?source=directory" title="Find out more about Code::Blocks"><h2>Code::Blocks</h2></a>',
 '<a itemprop="url" href="/projects/sweethome3d/?source=directory" title="Find out more about Sweet Home 3D"><h2>Sweet Home 3D</h2></a>',
 '<a itemprop="url" href="/projects/uberstudent/?source=directory" title="Find out more about UberStudent - Linux for Learners"><h2>UberStudent - Linux for Learners</h2></a>',
 '<a itemprop="url" href="/projects/movistartv/?source=directory" title="Find out more about movistartv"><h2>movistartv</h2></a>',
 '<a itemprop="url" href="/projects/tor-browser.mirror/?source=directory" title="Find out more about Tor Browser"><h2>Tor Browser</h2></a>',
 '<a itemprop="url" href="/projects/qbittorrent/?source=directory" title="Find out more about qBittorrent"><h2>qBittorrent</h2></a>',
 '<a itemprop="url" href="/projects/filezilla/?source=directory" title="Find out more about FileZilla®"><h2>FileZilla®</h2></a>',
 '<a itemprop="url" href="/projects/webadmin/?source=directory" title="Find out more about Webmin"><h2>Webmin</h2></a>',
 '<a itemprop="url" href="/projects/pinn/?source=directory" title="Find out more about PINN"><h2>PINN</h2></a>',
 '<a itemprop="url" href="/projects/opencvlibrary/?source=directory" title="Find out more about OpenCV"><h2>OpenCV</h2></a>']


def sourgehref(hreflist):
    dealhreflist = []
    pattern = re.compile(r'.*href=\"(.*?)\".*')
    for i in hreflist:
        result = pattern.findall(i)
        dealhreflist.append(result[0])
    return dealhreflist

print(sourgehref(hreflist))
