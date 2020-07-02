from canvasapi import Canvas
try:
    import modules.auth as auth
except:
    with open('modules/auth.py', 'w+') as f:
        # No auth py!
        f.writelines([('url = ""\n'), ('key = ""')])
        print("Fill in modules/auth.py and run this again!")
        exit()

if(auth.url == "" or auth.key == ""):
    print("You didn't put your Canvas URL or API key in modules/auth.py. Heck! You'll have to fix that and then come back here.")
    exit()
# initialize canvas!
try:
    canvasInstance = Canvas(auth.url, auth.key)
except: 
    print("We couldn't connect to Canvas. Check what you put in modules/auth.py and try again.")
    exit()

# get the currentUser.

user = canvasInstance.get_current_user()

print("Hello, " + user.name)

# get the user's courses.

coursesList = user.get_favorite_courses()

print("According to Canvas, you have favorited the following courses:")
for i in coursesList:
    print(i.name)
print("To change this, go to " + auth.url + "/courses and star the courses you'd like to export, then restart this script.")
input("Press enter to continue...")
print("We'll export each of these, one at a time, and then give you the links once the exports are all complete. You will recieve emails from Canvas as the exports complete, which is normal.")
print("Leave this window open.")
input("Press enter to continue...")
print("Let's go!")
exportURLs = {}

for i in coursesList:
    course = canvasInstance.get_course(i.id)
    try:
        courseExport = course.create_epub_export()
    except:
        print("Unfortunately, you don't have the permissions to export the course: " + course.name)
        exportURLs[course.name] = "Couldn't export this one"
        continue
    while(True):
        if(canvasInstance.get_progress(courseExport.epub_export['progress_id']).workflow_state == "completed"):
            link = course.get_epub_export(courseExport.epub_export['id']).epub_export['zip_attachment']['url']
            exportURLs[course.name] = link
            print(course.name + " export complete!")
            break
        else:
            print(course.name + ": " + canvasInstance.get_progress(courseExport.epub_export['progress_id']).workflow_state)
            continue

#print them links
print("All done! Here are the links:")
for i in coursesList:
    course = canvasInstance.get_course(i.id)
    print(course.name + ": " + exportURLs[course.name])
