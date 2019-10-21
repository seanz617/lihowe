$(function() {
        var menu = document.getElementById("aside")
        var fold = document.getElementById("btn")
        var info = document.getElementById("info")

        var tree = $('#jstree').jstree({
            // 引入插件
            'plugins': ['types','themes','contextmenu', "dnd","state", "wholerow"],
            'types': {
                'default': {
                    'icon': false  // 删除默认图标
                },
            },
            'checkbox': {  // 去除checkbox插件的默认效果
                'tie_selection': false,
                'keep_selected_style': false,
                'whole_node': false
            },
            'core': {
                "check_callback":true,
                'multiple' : true,  // 可否多选
                'data' : {{ productions | tojson }},  // 生成节点的数据，nodeData是后台返回的JSON数据
                'dblclick_toggle': true   //允许tree的双击展开
            },
            'contextmenu': {    // 右键菜单
                'items': {
                    'edit': {
                        'label': '编辑',
                        'action': function (data) {}
                    },
                    'delete': {
                        'label': '删除',
                        'action': function (data) {}
                    }
                }
            }
        });

        $('#jstree').bind("activate_node.jstree", function (obj, e) {
            if (e.node.id >= 1000) {
                full_node = $("#jstree").jstree(true).get_node(e.node)
                info.innerHTML = $("#jstree").jstree(true).get_path(full_node,">>")
            }
        });

        btn.onclick = function() {
            if (menu.offsetLeft == 0) {
                menu.style['margin-left'] = -300 + "px"
                fold.style['margin-left'] = 0 + "px"
                info.style['margin-left'] = 20 + "px"
            } else {
                menu.style['margin-left'] = 0 + "px"
                fold.style['margin-left'] = 300 + "px"
                info.style['margin-left'] = 320 + "px"
            }
        }
    });