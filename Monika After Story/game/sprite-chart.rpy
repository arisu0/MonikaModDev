# This defines a dynamic displayable for Monika whose position and style changes
# depending on the variables is_sitting and the function morning_flag
define is_sitting = True

image monika g1:
    "monika/g1.png"
    xoffset 35 yoffset 55
    parallel:
        zoom 1.00
        linear 0.10 zoom 1.03
        repeat
    parallel:
        xoffset 35
        0.20
        xoffset 0
        0.05
        xoffset -10
        0.05
        xoffset 0
        0.05
        xoffset -80
        0.05
        repeat
    time 1.25
    xoffset 0 yoffset 0 zoom 1.00
    "monika 3"

image monika g2:
    block:
        choice:
            "monika/g2.png"
        choice:
            "monika/g3.png"
        choice:
            "monika/g4.png"
    block:
        choice:
            pause 0.05
        choice:
            pause 0.1
        choice:
            pause 0.15
        choice:
            pause 0.2
    repeat

define m = DynamicCharacter('m_name', image='monika', what_prefix='"', what_suffix='"', ctc="ctc", ctc_position="fixed")

init -1 python in mas_sprites:
    # specific image generation functions

    # main art path
    MOD_ART_PATH = "mod_assets/monika/"
    STOCK_ART_PATH = "monika/"

    # delimiters
    ART_DLM = "-"

    # important keywords
    KW_STOCK_ART = "def"

    ### other paths:
    # H - hair (and body by connection)
    # C - clothing
    # T - sitting
    # S - standing
    # F - face parts
    # A - accessories
    C_MAIN = MOD_ART_PATH + "c/"
    F_MAIN = MOD_ART_PATH + "f/"
    A_MAIN = MOD_ART_PATH + "a/"
    S_MAIN = MOD_ART_PATH + "s/"

    # sitting standing parts
#    S_MAIN = "standing/"

    # facial parts
    F_T_MAIN = F_MAIN
#    F_S_MAIN = F_MAIN + S_MAIN
    
    # accessories parts
    A_T_MAIN = A_MAIN

    ### End paths

    # location stuff for some of the compsoite
    LOC_REG = "(1280, 850)"
    LOC_LEAN = "(1280, 742)"
    LOC_Z = "(0, 0)"
    LOC_STAND = "(960, 960)"

    # composite stuff
    I_COMP = "im.Composite"
    L_COMP = "LiveComposite"
    TRAN = "Transform"

    # zoom
    ZOOM = "zoom=1.25"

    # Prefixes for files
    PREFIX_BODY = "torso" + ART_DLM
    PREFIX_ARMS = "arms" + ART_DLM
    PREFIX_BODY_LEAN = "torso-leaning" + ART_DLM
    PREFIX_FACE = "face" + ART_DLM
    PREFIX_FACE_LEAN = "face-leaning" + ART_DLM
    PREFIX_ACS = "acs" + ART_DLM
    PREFIX_ACS_LEAN = "acs-leaning" + ART_DLM
    PREFIX_EYEB = "eyebrows" + ART_DLM
    PREFIX_EYES = "eyes" + ART_DLM
    PREFIX_NOSE = "nose" + ART_DLM
    PREFIX_MOUTH = "mouth" + ART_DLM
    PREFIX_SWEAT = "sweatdrop" + ART_DLM
    PREFIX_EMOTE = "emote" + ART_DLM
    PREFIX_TEARS = "tears" + ART_DLM
    PREFIX_EYEG = "eyebags" + ART_DLM
    PREFIX_BLUSH = "blush" + ART_DLM

    # suffixes
    NIGHT_SUFFIX = ART_DLM + "n"
    FILE_EXT = ".png"


    def acs_lean_mode(lean):
        """
        Returns the appropriate accessory prefix dpenedong on lean

        IN:
            lean - type of lean

        RETURNS:
            appropratie accessory prefix
        """
        if lean:
            return "".join([PREFIX_ACS_LEAN, lean, ART_DLM])

        return PREFIX_ACS


    def face_lean_mode(lean):
        """
        Returns the appropriate face prefix depending on lean

        IN:
            lean - type of lean

        RETURNS:
            appropriate face prefix
        """
        if lean:
            return "".join([PREFIX_FACE_LEAN, lean, ART_DLM])

        return PREFIX_FACE


    def night_mode(isnight):
        """
        Returns the appropriate night string
        """
        if isnight:
            return NIGHT_SUFFIX

        return ""


    # sprite maker functions


    def _ms_accessory(acs, isnight, issitting, lean=None):
        """
        Creates accessory string

        IN:
            acs - MASAccessory object
            isnight - True will generate night string, false will not
            issitting - True will use sitting pic, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            accessory string
        """
        if issitting:
            acs_str = acs.sit

        else:
            acs_str = acs.stand

        return "".join([
            LOC_Z,
            ',"',
            A_T_MAIN,
            acs_lean_mode(lean),
            acs_str,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_accessorylist(acs_list, isnight, issitting, lean=None):
        """
        Creates accessory strings for a list of accessories

        IN:
            acs_list - list of MASAccessory object, in order of rendering
            isnight - True will generate night string, false will not
            issitting - True will use sitting pic, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            accessory string list
        """
        if len(acs_list) == 0:
            return ""
            
        return "," + ",".join([
            _ms_accessory(acs, isnight, issitting, lean=lean)
            for acs in acs_list
        ])


    def _ms_arms(clothing, hair, arms, isnight):
        """
        Creates arms string

        IN:
            clothing - type of clothing
            hair - type of hair
            arms - type of arms
            isnight - True will generate night string, false will not

        RETURNS:
            arms string
        """
        return "".join([
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_ARMS,
            hair,
            ART_DLM,
            arms,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_blush(blush, isnight, lean=None):
        """
        Creates blush string

        IN:
            blush - type of blush
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            blush string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_BLUSH,
            blush,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_body(clothing, hair, isnight, lean=None, arms=""):
        """
        Creates body string

        IN:
            clothing - type of clothing
            hair - type of hair
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)
            arms - type of arms
                (Default: "")

        RETURNS:
            body string
        """
        if lean:
            # leaning is a single parter
            body_str = ",".join([
                LOC_LEAN,
                _ms_torsoleaning(clothing, hair, lean, isnight)
            ])

        else:
            # not leaning is a 2parter
            body_str = ",".join([
                LOC_REG,
                _ms_torso(clothing, hair, isnight),
                _ms_arms(clothing, hair, arms, isnight)
            ])

        # add the rest of the parts
        return "".join([
            I_COMP,
            "(",
            body_str,
            ")"
        ])


    def _ms_emote(emote, isnight, lean=None):
        """
        Creates emote string

        IN:
            emote - type of emote
            isnight - True will generate night string, false will not
            lean - type of lean
                (Dfeualt: None)

        RETURNS:
            emote string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EMOTE,
            emote,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_eyebags(eyebags, isnight, lean=None):
        """
        Creates eyebags string

        IN:
            eyebags - type of eyebags
            isnight - True will generate night string, false will not
            lean - type of lean
                (Dfeault: None)

        RETURNS:
            eyebags string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EYEG,
            eyebags,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_eyebrows(eyebrows, isnight, lean=None):
        """
        Creates eyebrow string

        IN:
            eyebrows - type of eyebrows
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            eyebrows string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EYEB,
            eyebrows,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_eyes(eyes, isnight, lean=None):
        """
        Creates eyes string

        IN:
            eyes - type of eyes
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            eyes stirng
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_EYES,
            eyes,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])
            

    def _ms_face(
            eyebrows, 
            eyes, 
            nose, 
            mouth, 
            isnight, 
            lean=None,
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None
        ):
        """
        Create face string
        (the order these are drawn are in order of argument)

        IN:
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            isnight - True will generate a night string, false will not
            lean - type of lean
                (Default: None)
            eyebags - type of eyebags
                (Default: None)
            sweat - type of sweat drop
                (Default: None)
            blush - type of blush
                (Default: None)
            tears - type of tears
                (Default: None)
            emote - type of emote
                (Default: None)

        RETURNS:
            face string
        """
        subparts = list()

        # lean checking
        if lean:
            subparts.append(LOC_LEAN)

        else:
            subparts.append(LOC_REG)
            
        # now for the required parts
        subparts.append(_ms_eyebrows(eyebrows, isnight, lean=lean))
        subparts.append(_ms_eyes(eyes, isnight, lean=lean))
        subparts.append(_ms_nose(nose, isnight, lean=lean))
        subparts.append(_ms_mouth(mouth, isnight, lean=lean))

        # and optional parts
        if eyebags:
            subparts.append(_ms_eyebags(eyebags, isnight, lean=lean))

        if sweat:
            subparts.append(_ms_sweat(sweat, isnight, lean=lean))

        if blush:
            subparts.append(_ms_blush(blush, isnight, lean=lean))

        if tears:
            subparts.append(_ms_tears(tears, isnight, lean=lean))

        if emote:
            subparts.append(_ms_emote(emote, isnight, lean=lean))

        # alright, now build the face string
        return "".join([
            I_COMP,
            "(",
            ",".join(subparts),
            ")"
        ])


    def _ms_head(clothing, hair, head):
        """
        Creates head string

        IN:
            clothing - type of clothing
            hair - type of hair
            head - type of head

        RETURNS:
            head string
        """
        # NOTE: untested
        return "".join([
            LOC_Z,
            ',"',
            S_MAIN,
            clothing,
            "/",
            hair,
            ART_DLM,
            head,
            FILE_EXT,
            '"'
        ])


    def _ms_left(clothing, hair, left):
        """
        Creates left side string

        IN:
            clothing - type of clothing
            hair - type of hair
            left - type of left side

        RETURNS:
            left side stirng
        """
        # NOTE UNTESTED
        return "".join([
            LOC_Z,
            ',"',
            S_MAIN,
            clothing,
            "/",
            hair,
            ART_DLM,
            left,
            FILE_EXT,
            '"'
        ])


    def _ms_mouth(mouth, isnight, lean=None):
        """
        Creates mouth string

        IN:
            mouth - type of mouse
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            mouth string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_MOUTH,
            mouth,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_nose(nose, isnight, lean=None):
        """
        Creates nose string

        IN:
            nose - type of nose
            isnight - True will genreate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            nose string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_NOSE,
            nose,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_right(clothing, hair, right):
        """
        Creates right body string

        IN:
            clothing - type of clothing
            hair - type of hair
            right - type of right side

        RETURNS:
            right body string
        """
        # NOTE: UNTESTED
        return "".join([
            LOC_Z,
            ',"',
            S_MAIN,
            clothing,
            "/",
            hair,
            ART_DLM,
            head,
            FILE_EXT,
            '"'
        ])


    def _ms_sitting(
            clothing, 
            hair,
            eyebrows,
            eyes,
            nose,
            mouth,
            isnight,
            acs_list,
            lean=None,
            arms="",
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None
        ):
        """
        Creates sitting string

        IN:
            clothing - type of clothing
            hair - type of hair
            eyebrows - type of eyebrows
            eyes - type of eyes
            nose - type of nose
            mouth - type of mouth
            isnight - True will genreate night string, false will not
            acs_list - list of MASAccessory objects to draw
            lean - type of lean
                (Default: None)
            arms - type of arms
                (Default: "")
            eyebags - type of eyebags
                (Default: None)
            sweat - type of sweatdrop
                (Default: None)
            blush - type of blush
                (Default: None)
            tears - type of tears
                (Default: None)
            emote - type of emote
                (Default: None)

        RETURNS:
            sitting stirng
        """
        if lean:
            loc_str = LOC_LEAN

        else:
            loc_str = LOC_REG

        return "".join([
            TRAN,
            "(",
            L_COMP,
            "(",
            loc_str,
            ",",
            LOC_Z,
            ",",
            _ms_body(clothing, hair, isnight, lean=lean, arms=arms),
            ",",
            LOC_Z,
            ",",
            _ms_face(
                eyebrows,
                eyes,
                nose,
                mouth,
                isnight,
                lean=lean,
                eyebags=eyebags,
                sweat=sweat,
                blush=blush,
                tears=tears,
                emote=emote
            ),
            _ms_accessorylist(acs_list, isnight, True, lean=lean),
            "),",
            ZOOM,
            ")"
        ])


    def _ms_standing(clothing, hair, head, left, right, acs_list):
        """
        Creates the custom standing string
        This is different than the stock ones because of image location

        IN:
            clothing - type of clothing
            hair - type of hair
            head - type of head
            left - type of left side
            right - type of right side
            acs_list - list of MASAccessory objects

        RETURNS:
            custom standing sprite
        """
        # NOTE: UNTESTED
        return "".join([
            I_COMP,
            "(",
            LOC_STAND,
            ",",
            _ms_left(clothing, hair, left),
            ",",
            _ms_right(clothing, hair, right),
            ",",
            _ms_head(clothing, hair, head),
            _ms_accessorylist(acs_list, False, False),
            ")"
        ])


    def _ms_standingstock(head, left, right, acs_list, single=None):
        """
        Creates the stock standing string
        This is different then the custom ones because of image location

        Also no night version atm.

        IN:
            head - type of head
            left - type of left side
            right - type of right side
            acs_list - list of MASAccessory objects
            single - type of single standing picture. 
                (Defualt: None)

        RETURNS:
            stock standing string
        """
        if single:
            return "".join([
                I_COMP,
                "(",
                LOC_STAND,
                ",",
                LOC_Z,
                ',"',
                STOCK_ART_PATH,
                single,
                FILE_EXT,
                '"',
                _ms_accessorylist(acs_list, False, False),
                ")"
            ])

        return "".join([
            I_COMP,
            "(",
            LOC_STAND,
            ",",
            LOC_Z,
            ',"',
            STOCK_ART_PATH,
            left,
            FILE_EXT,
            '",',
            LOC_Z,
            ',"',
            STOCK_ART_PATH,
            right,
            FILE_EXT,
            '",',
            LOC_Z,
            ',"',
            STOCK_ART_PATH,
            head,
            FILE_EXT,
            '"',
            _ms_accessorylist(acs_list, False, False),
            ")"
        ])


    def _ms_sweat(sweat, isnight, lean=None):
        """
        Creates sweatdrop string
    
        IN:
            sweat -  type of sweatdrop
            isnight - True will generate night string, false will not
            lean - type of lean
                (Defualt: None)

        RETURNS:
            sweatdrop string
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_SWEAT,
            sweat,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_tears(tears, isnight, lean=None):
        """
        Creates tear string

        IN:
            tears - type of tears
            isnight - True will generate night string, false will not
            lean - type of lean
                (Default: None)

        RETURNS:
            tear strring
        """
        return "".join([
            LOC_Z,
            ',"',
            F_T_MAIN,
            face_lean_mode(lean),
            PREFIX_TEARS,
            tears,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_torso(clothing, hair, isnight):
        """
        Creates torso string

        IN:
            clothing - type of clothing
            hair - type of hair
            isnight - True will generate night string, false will not

        RETURNS:
            torso string
        """
        return "".join([
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_BODY,
            hair,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])


    def _ms_torsoleaning(clothing, hair, lean, isnight):
        """
        Creates leaning torso string

        IN:
            clothing - type of clothing
            hair - type of ahri
            lean - type of leaning
            isnight - True will genreate night string, false will not

        RETURNS:
            leaning torso string
        """
        return "".join([
            LOC_Z,
            ',"',
            C_MAIN,
            clothing,
            "/",
            PREFIX_BODY_LEAN,
            hair,
            ART_DLM,
            lean,
            night_mode(isnight),
            FILE_EXT,
            '"'
        ])

            
# Dynamic sprite builder
# retrieved from a Dress Up Renpy Cookbook
# https://lemmasoft.renai.us/forums/viewtopic.php?f=51&t=30643

init -2 python:
#    import renpy.store as store
#    import renpy.exports as renpy # we need this so Ren'Py properly handles rollback with classes
#    from operator import attrgetter # we need this for sorting items
    import math

    # Monika character base
    class MASMonika(renpy.store.object):
        def __init__(self):
            self.name="Monika"
            self.haircut="default"
            self.haircolor="default"
            self.skin_hue=0 # monika probably doesn't have different skin color
            self.lipstick="default" # i guess no lipstick
            self.clothes = "def" # default clothes is school outfit
            self.hair = "def" # default hair is the usual whtie ribbon
            self.acs = [] # accesories
            self.hair_hue=0 # hair color?
           
        
        def change_clothes(self, new_cloth):
            """
            Changes clothes to the given cloth

            IN:
                new_cloth - new clothes to wear
            """
            self.clothes = new_cloth

        
        def change_hair(self, new_hair):
            """
            Changes hair to the given hair

            IN:
                new_hair - new hair to wear
            """
            self.hair = new_hair


        def change_outfit(self, new_cloth, new_hair):
            """
            Changes both clothes and hair

            IN:
                new_cloth - new clothes to wear
                new_hair - new hair to wear
            """
            self.change_clothes(new_cloth)
            self.change_hair(new_hair)


        def get_outfit(self):
            """
            Returns the current outfit

            RETURNS:
                tuple:
                    [0] - current clothes
                    [1] - current hair
            """
            return (self.clothes, self.hair)


        def is_wearing_acs(self, accessory):
            """
            Checks if currently wearing the given accessory

            IN:
                accessory - accessory to check

            RETURNS:
                True if wearing accessory, false if not
            """
            return accessory in self.acs


        def reset_all(self):
            """
            Resets all of monika
            """
            self.reset_clothes()
            self.reset_hair()
            self.remove_all_acs()


        def remove_acs(self, accessory):
            """
            Removes the given accessory

            IN:
                accessory - accessory to remove
            """
            if accessory in self.acs:
                self.acs.remove(accessory)


        def remove_all_acs(self):
            """
            Removes all accessories
            """
            self.acs = list()


        def reset_clothes(self):
            """
            Resets clothing to default
            """
            self.clothes = "def"


        def reset_hair(self):
            """
            Resets hair to default
            """
            self.hair = "def"


        def reset_outfit(self):
            """
            Resetse clothing and hair to default
            """
            self.reset_clothes()
            self.reset_hair()

       
        def wear_acs(self, accessory):
            """
            Wears the given accessory

            IN:
                accessory - accessory to wear
            """
            self.acs.wear(accessory)
        

    # hues, probably not going to use these
    hair_hue1 = im.matrix([ 1, 0, 0, 0, 0,
                        0, 1, 0, 0, 0,
                        0, 0, 1, 0, 0,
                        0, 0, 0, 1, 0 ])
    hair_hue2 = im.matrix([ 3.734, 0, 0, 0, 0,
                        0, 3.531, 0, 0, 0,
                        0, 0, 1.375, 0, 0,
                        0, 0, 0, 1, 0 ])
    hair_hue3 = im.matrix([ 3.718, 0, 0, 0, 0,
                        0, 3.703, 0, 0, 0,
                        0, 0, 3.781, 0, 0,
                        0, 0, 0, 1, 0 ])
    hair_hue4 = im.matrix([ 3.906, 0, 0, 0, 0,
                        0, 3.671, 0, 0, 0,
                        0, 0, 3.375, 0, 0,
                        0, 0, 0, 1, 0 ])
    skin_hue1 = hair_hue1
    skin_hue2 = im.matrix([ 0.925, 0, 0, 0, 0,
                        0, 0.840, 0, 0, 0,
                        0, 0, 0.806, 0, 0,
                        0, 0, 0, 1, 0 ])
    skin_hue3 = im.matrix([ 0.851, 0, 0, 0, 0,
                        0, 0.633, 0, 0, 0,
                        0, 0, 0.542, 0, 0,
                        0, 0, 0, 1, 0 ])
        
    hair_huearray = [hair_hue1,hair_hue2,hair_hue3,hair_hue4]
    
    skin_huearray = [skin_hue1,skin_hue2,skin_hue3]
            
   
    # instead of clothes, these are accessories
    class MASAccessory(renpy.store.object):
        def __init__(self, 
                name, 
                sit,
                stand=None,
                priority=10,
                can_strip=True
            ):
            self.name=name
            self.sit = sit
            if stand is None:
                stand = sit
            self.stand = stand
            self.priority=priority

            # this is for "Special Effects" like a scar or a wound, that 
            # shouldn't be removed by undressing.
            self.can_strip=can_strip 
          
        @staticmethod
        def get_priority(acs):
            """
            Gets the priority of the given accessory

            This is for sorting
            """
            return acs.priority

     
    # The main drawing function...
    def mas_drawmonika(
            st,
            at,
            character,

            # requried sitting parts
            eyebrows,
            eyes,
            nose,
            mouth,

            # required standing parts
            head,
            left,
            right,

            # optional sitting parts
            lean=None,
            arms="",
            eyebags=None,
            sweat=None,
            blush=None,
            tears=None,
            emote=None,

            # optional standing parts
            stock=True
            single=None
        ):
        """
        Draws monika dynamically
        NOTE: custom standing stuff not ready for usage yet.
        NOTE: the actual drawing of accessories happens in the respective
            functions instead of here.
        NOTE: because of how clothes, hair, and body is tied together,
            monika can only have 1 type of clothing and 1 hair style
            at a time.

        IN:
            st - renpy related
            at - renpy related
            character - MASMonika character object
            eyebrows - type of eyebrows (sitting)
            eyes - type of eyes (sitting)
            nose - type of nose (sitting)
            mouth - type of mouth (sitting)
            head - type of head (standing)
            left - type of left side (standing)
            right - type of right side (standing)
            lean - type of lean (sitting)
                (Default: None)
            arms - type of arms (sitting)
                (Default: "")
            eyebags - type of eyebags (sitting)
                (Default: None)
            sweat - type of sweatdrop (sitting)
                (Default: None)
            blush - type of blush (sitting)
                (Default: None)
            tears - type of tears (sitting)
                (Default: None)
            emote - type of emote (sitting)
                (Default: None)
            stock - True means we are using stock standing, False means not
                (standing)
                (Default: True)
            single - type of single standing image (standing)
                (Default: None)
        """
        
        # accessories have a priority
        acs_list=sorted(character.acs, key=MASAccessory.get_priority) 
 
        # are we sitting or not
        if is_sitting:
            cmd = store.mas_sprites._ms_sitting(
                character.clothes,
                character.hair,
                eyebrows,
                eyes,
                nose,
                mouth,
                not morning_flag,
                acs_list,
                lean=lean,
                arms=arms,
                eyebags=eyebags,
                sweat=sweat,
                blush=blush,
                tears=tears,
                emote=emote
            )

        else: 
        # TODO change this to an elif and else the custom stnading mode
#        elif stock: 
            # stock standing mode
            cmd = store.mas_sprites._ms_standingstock(
                head,
                left,
                right,
                acs_list,
                single=single
            )

#        else:
            # custom standing mode
            
        return eval(cmd),None # Unless you're using animations, you can set refresh rate to None
        
#body poses
image body_1 = im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-steepling.png")
image body_1_n = im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-steepling-n.png")
image body_2 = im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-crossed.png")
image body_2_n = im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-crossed-n.png")
image body_3 = im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-restleftpointright.png")
image body_3_n = im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-restleftpointright-n.png")
image body_4 = im.Composite((1280,850),(0,0),"mod_assets/monika/torso.png",(0,0),"mod_assets/monika/arms-pointright.png")
image body_4_n = im.Composite((1280,850),(0,0),"mod_assets/monika/torso-n.png",(0,0),"mod_assets/monika/arms-pointright-n.png")
image body_5 = im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning.png")
image body_5_n = im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning-n.png")

#faces
image face_s = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png")
image face_s_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png")
image face_a = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png")
image face_a_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png")
image face_b = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-big.png")
image face_b_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-big-n.png")
image face_c = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png")
image face_c_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png")
image face_d = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png")
image face_d_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png")
image face_e = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png")
image face_e_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png")
image face_f = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png")
image face_f_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png")
image face_g = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png")
image face_g_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png")
image face_h = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png")
image face_h_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png")
image face_i = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-normal.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png")
image face_i_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-normal-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png")
image face_j = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png")
image face_j_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png")
image face_k = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up.png",(0,0),"mod_assets/monika/face-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-big.png")
image face_k_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-big-n.png")
image face_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-big.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-big-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_m = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-left.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smile.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_m_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-left-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smile-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-left.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-big.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_n_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-left-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-big-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_o = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-left.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_o_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-left-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_p = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit.png",(0,0),"mod_assets/monika/face-eyes-left.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png",(0,0),"mod_assets/monika/face-sweatdrop.png")
image face_p_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-eyes-left-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png",(0,0),"mod_assets/monika/face-sweatdrop-n.png")
image face_q = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-closedsad.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-smirk.png")
image face_q_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-closedsad-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-smirk-n.png")
image face_r = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid.png",(0,0),"mod_assets/monika/face-eyes-closedsad.png",(0,0),"mod_assets/monika/face-nose.png",(0,0),"mod_assets/monika/face-mouth-small.png")
image face_r_n = im.Composite((1280,850),(0,0),"mod_assets/monika/face-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-eyes-closedsad-n.png",(0,0),"mod_assets/monika/face-nose-n.png",(0,0),"mod_assets/monika/face-mouth-small-n.png")

image face_s_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png")
image face_s_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png")
image face_a_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png")
image face_a_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png")
image face_b_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-big.png")
image face_b_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-big-n.png")
image face_c_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk.png")
image face_c_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_d_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small.png")
image face_d_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")
image face_e_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png")
image face_e_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png")
image face_f_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk.png")
image face_f_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_g_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small.png")
image face_g_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")
image face_h_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk.png")
image face_h_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_i_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small.png")
image face_i_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-normal-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")
image face_j_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png")
image face_j_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png")
image face_k_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-big.png")
image face_k_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-up-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-big-n.png")
image face_l_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-big.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_l_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedhappy-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-big-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_m_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-left.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_m_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-left-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smile-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_n_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-left.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-big.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_n_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-left-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-big-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_o_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-left.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_o_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-left-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_p_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit.png",(0,0),"mod_assets/monika/face-leaning-eyes-left.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop.png")
image face_p_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-knit-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-left-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png",(0,0),"mod_assets/monika/face-leaning-sweatdrop-n.png")
image face_q_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedsad.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_q_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedsad-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-smirk-n.png")
image face_r_l = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedsad.png",(0,0),"mod_assets/monika/face-leaning-nose.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")
image face_r_l_n = im.Composite((1280,742),(0,0),"mod_assets/monika/face-leaning-eyebrows-mid-n.png",(0,0),"mod_assets/monika/face-leaning-eyes-closedsad-n.png",(0,0),"mod_assets/monika/face-leaning-nose-n.png",(0,0),"mod_assets/monika/face-leaning-mouth-small-n.png")

# Monika
define monika_chr = MASMonika()

image monika 1 = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 2 = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 3 = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 4 = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="2r",
    arms="pointright"
)

image monika 5 = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="",
    left="",
    right="",
    lean="def",
    arms="pointright",
    single="3a"
)

image monika 1a = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1b = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1c = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1d = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1e = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1f = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1g = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1h = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1i = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1j = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1k = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1l = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1m = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1n = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1o = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1p = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="1r",
    arms="steepling",
    sweat="def"
)

image monika 1q = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 1r = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="1r",
    arms="steepling"
)

image monika 2a = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2b = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2c = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2d = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2e = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2f = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2g = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2h = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2i = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2j = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2k = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2l = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2m = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2n = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2o = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2p = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="1l",
    right="2r",
    arms="crossed",
    sweat="def"
)

image monika 2q = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 2r = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="1l",
    right="2r",
    arms="crossed"
)

image monika 3a = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="a",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3b = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="big",
    head="b",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3c = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="c",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3d = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="normal",
    nose="def",
    mouth="small",
    head="d",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3e = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smile",
    head="e",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3f = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="f",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3g = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="normal",
    nose="def",
    mouth="small",
    head="g",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3h = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="smirk",
    head="h",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3i = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="normal",
    nose="def",
    mouth="small",
    head="i",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3j = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="smile",
    head="j",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3k = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="up",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="k",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3l = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="closedhappy",
    nose="def",
    mouth="big",
    head="l",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3m = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smile",
    head="m",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3n = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="big",
    head="n",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3o = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="smirk",
    head="o",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3p = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="knit",
    eyes="left",
    nose="def",
    mouth="small",
    head="p",
    left="2l",
    right="1r",
    arms="restleftpointright",
    sweat="def"
)

image monika 3q = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="smirk",
    head="q",
    left="2l",
    right="1r",
    arms="restleftpointright"
)

image monika 3r = DynamicDisplayable(
    mas_drawmonika, 
    character=monika_chr, 
    eyebrows="mid",
    eyes="closedsad",
    nose="def",
    mouth="small",
    head="r",
    left="2l",
    right="1r",
    arms="restleftpointright"
)



image monika 4a = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_a"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_a_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/a.png")
            )
image monika 4b = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_b"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_b_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/b.png")
            )
image monika 4c = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_c"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_c_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/c.png")
            )
image monika 4d = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_d"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_d_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/d.png")
            )
image monika 4e = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_e"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_e_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/e.png")
            )
image monika 4f = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_f"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_f_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/f.png")
            )
image monika 4g = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_g"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_g_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/g.png")
            )
image monika 4h = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_h"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_h_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/h.png")
            )
image monika 4i = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_i"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_i_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/i.png")
            )
image monika 4j = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_j"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_j_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/j.png")
            )
image monika 4k = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_k"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_k_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/k.png")
            )
image monika 4l = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/l.png")
            )
image monika 4m = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_m"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_m_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/m.png")
            )
image monika 4n = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_n"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_n_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/n.png")
            )
image monika 4o = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_o"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_o_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/o.png")
            )
image monika 4p = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_p"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_p_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/p.png")
            )
image monika 4q = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_q"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_q_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/q.png")
            )
image monika 4r = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4",(0,0),"face_r"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,850),(0,0),"body_4_n",(0,0),"face_r_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/2l.png", (0, 0), "monika/2r.png", (0, 0), "monika/r.png")
            )

image monika 5a = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5",(0,0),"face_a_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5_n",(0,0),"face_a_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/3a.png")
            )
image monika 5b = ConditionSwitch(
            'is_sitting and morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5",(0,0),"face_h_l"),zoom=1.25),
            'is_sitting and not morning_flag',Transform(LiveComposite((1280,742),(0,0),"body_5_n",(0,0),"face_h_l_n"),zoom=1.25),
            'not is_sitting',im.Composite((960, 960), (0, 0), "monika/3b.png")
            )

