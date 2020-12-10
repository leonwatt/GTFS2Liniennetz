class ColorScheme:
    line_colors = ["#BB3636", "#FF5B1A", "#EEF608", "#A9C539", "#0CC261", "#39C5C3", "#2D80D3", "#8478F4", "#D66ECD"]
    background_color = "#222B38"
    override_route_colors = False
    light_background = False


def winterColors():
    colors = ColorScheme()
    colors.line_colors = ["#98CCD3", "#489DA8", "#29E6FF", "#D3C698", "#24A26C", "#8EDDA1", "#5C99E4", "#FFFFFF", "#F0D77B", "#DFA833"]
    colors.background_color = "#42576D"
    return colors


def springColors():
    colors = ColorScheme()
    colors.line_colors = ["#6F2F6D", "#CF38CA", "#DA2828", "#0288C5", "#4F7C35", "#FFED22", "#E7E7E7", "#522351", "#40B8E0", "#487FBD"]
    colors.background_color = "#A9C539"
    return colors

def lightColors():
    colors = ColorScheme()
    colors.line_colors = ["#AA4949", "#CF4323", "#FD5A5A", "#DAAA19", "#EECE3E", "#FD943E", "#6CBA1D", "#A0D992", "#3C8929", "#20A9BE", "#1C94A6", "#1D6872", "#4276DE", "#839BCA", "#4967AA", "#9D5ACD", "#BC8EDD", "#7122A9", "#E45CA7", "#FF8DCC", "#C02078"]
    colors.background_color = "#C7C7C7"
    colors.light_background = True
    return colors