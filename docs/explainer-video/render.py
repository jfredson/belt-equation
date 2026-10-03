import sys, base64, subprocess
from playwright.sync_api import sync_playwright
FPS=30
# (real seconds, scene seconds): flat runs are reading holds, shallow runs are slowed builds
KNOTS=[(0,0),(8.5,4.4),(14.4,8.6),(15.3,9.5),(18.8,9.5),(50.7,41.4)]
DUR=KNOTS[-1][0]
def scene_t(T):
    for (r0,s0),(r1,s1) in zip(KNOTS,KNOTS[1:]):
        if T<=r1: return s0+(s1-s0)*(T-r0)/(r1-r0)
    return KNOTS[-1][1]
mode=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    import os; pg.goto('file://'+os.path.join(os.path.dirname(os.path.abspath(__file__)),'scene.html')); pg.evaluate('window.ready'); pg.wait_for_timeout(300)
    def frame(T):
        d=pg.evaluate(f"render({scene_t(T)},{T},{T}); document.getElementById('c').toDataURL('image/png')")
        return base64.b64decode(d.split(',',1)[1])
    if mode=='stills':
        for T in [50.6]:
            open(f'still_{T:05.2f}.png','wb').write(frame(T))
    else:
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-i','-',
            '-c:v','libx264','-preset','slow','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',sys.argv[2]],stdin=subprocess.PIPE)
        n=int(DUR*FPS)
        for i in range(n):
            ff.stdin.write(frame(i/FPS))
        ff.stdin.close(); ff.wait()
    b.close()
