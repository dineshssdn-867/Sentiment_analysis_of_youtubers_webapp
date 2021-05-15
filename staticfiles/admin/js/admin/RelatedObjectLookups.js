"use strict";{const e=django.jQuery;function showAdminPopup(e,t,o){const n=e.id.replace(t,""),s=new URL(e.href);return o&&s.searchParams.set("_popup",1),window.open(s,n,"height=500,width=800,resizable=yes,scrollbars=yes").focus(),!1}function showRelatedObjectLookupPopup(e){return showAdminPopup(e,/^lookup_/,!0)}function dismissRelatedLookupPopup(e,t){const o=e.name,n=document.getElementById(o);n.classList.contains("vManyToManyRawIdAdminField")&&n.value?n.value+=","+t:document.getElementById(o).value=t,e.close()}function showRelatedObjectPopup(e){return showAdminPopup(e,/^(change|add|delete)_/,!1)}function updateRelatedObjectLinks(t){const o=e(t),n=o.nextAll(".view-related, .change-related, .delete-related");if(!n.length)return;const s=o.val();s?n.each(function(){const t=e(this);t.attr("href",t.attr("data-href-template").replace("__fk__",s))}):n.removeAttr("href")}function dismissAddRelatedObjectPopup(t,o,n){const s=t.name,d=document.getElementById(s);if(d){const t=d.nodeName.toUpperCase();"SELECT"===t?d.options[d.options.length]=new Option(n,o,!0,!0):"INPUT"===t&&(d.classList.contains("vManyToManyRawIdAdminField")&&d.value?d.value+=","+o:d.value=o),e(d).trigger("change")}else{const e=s+"_to",t=new Option(n,o);SelectBox.add_to_cache(e,t),SelectBox.redisplay(e)}t.close()}function dismissChangeRelatedObjectPopup(t,o,n,s){const d=t.name.replace(/^edit_/,""),i=interpolate("#%s, #%s_from, #%s_to",[d,d,d]),a=e(i);a.find("option").each(function(){this.value===o&&(this.textContent=n,this.value=s)}),a.next().find(".select2-selection__rendered").each(function(){this.lastChild.textContent=n,this.title=n}),t.close()}function dismissDeleteRelatedObjectPopup(t,o){const n=t.name.replace(/^delete_/,""),s=interpolate("#%s, #%s_from, #%s_to",[n,n,n]);e(s).find("option").each(function(){this.value===o&&e(this).remove()}).trigger("change"),t.close()}window.showRelatedObjectLookupPopup=showRelatedObjectLookupPopup,window.dismissRelatedLookupPopup=dismissRelatedLookupPopup,window.showRelatedObjectPopup=showRelatedObjectPopup,window.updateRelatedObjectLinks=updateRelatedObjectLinks,window.dismissAddRelatedObjectPopup=dismissAddRelatedObjectPopup,window.dismissChangeRelatedObjectPopup=dismissChangeRelatedObjectPopup,window.dismissDeleteRelatedObjectPopup=dismissDeleteRelatedObjectPopup,window.showAddAnotherPopup=showRelatedObjectPopup,window.dismissAddAnotherPopup=dismissAddRelatedObjectPopup,e(document).ready(function(){e("a[data-popup-opener]").on("click",function(t){t.preventDefault(),opener.dismissRelatedLookupPopup(window,e(this).data("popup-opener"))}),e("body").on("click",".related-widget-wrapper-link",function(t){if(t.preventDefault(),this.href){const t=e.Event("django:show-related",{href:this.href});e(this).trigger(t),t.isDefaultPrevented()||showRelatedObjectPopup(this)}}),e("body").on("change",".related-widget-wrapper select",function(t){const o=e.Event("django:update-related");e(this).trigger(o),o.isDefaultPrevented()||updateRelatedObjectLinks(this)}),e(".related-widget-wrapper select").trigger("change"),e("body").on("click",".related-lookup",function(t){t.preventDefault();const o=e.Event("django:lookup-related");e(this).trigger(o),o.isDefaultPrevented()||showRelatedObjectLookupPopup(this)})})}