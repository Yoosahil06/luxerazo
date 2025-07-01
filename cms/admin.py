
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Banner, Blog, PromotionalBlock, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author_name', 'author_email', 'content', 'is_approved', 'created_at')
    readonly_fields = ('created_at',)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'display_date_range', 'order', 'is_currently_active')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'subtitle')
    ordering = ('order', '-created_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'image', 'link_url')
        }),
        ('Display Settings', {
            'fields': ('status', 'start_date', 'end_date', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')

    def display_date_range(self, obj):
        if obj.start_date and obj.end_date:
            return f"{obj.start_date.strftime('%Y-%m-%d')} to {obj.end_date.strftime('%Y-%m-%d')}"
        return "No date range set"
    display_date_range.short_description = "Schedule"

    def is_currently_active(self, obj):
        is_active = obj.is_active
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if is_active else 'red',
            'Active' if is_active else 'Inactive'
        )
    is_currently_active.short_description = "Active Status"

class PromotionalBlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'display_date_range', 'is_active')
    list_filter = ('position', 'is_active', 'created_at')
    search_fields = ('title', 'content')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content')
        }),
        ('Display Settings', {
            'fields': ('position', 'start_date', 'end_date', 'is_active')
        }),
        ('Styling', {
            'fields': ('background_color', 'text_color'),
            'classes': ('collapse',)
        })
    )

    def display_date_range(self, obj):
        if obj.start_date and obj.end_date:
            return f"{obj.start_date.strftime('%Y-%m-%d')} to {obj.end_date.strftime('%Y-%m-%d')}"
        return "No date range set"
    display_date_range.short_description = "Schedule"

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'publish_date', 'featured', 'comment_count')
    list_filter = ('status', 'featured', 'allow_comments', 'created_at')
    search_fields = ('title', 'content', 'meta_keywords')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle', 'slug', 'content', 'excerpt', 'image')
        }),
        ('Publishing', {
            'fields': ('author', 'status', 'publish_date', 'featured', 'allow_comments')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        })
    )

    def comment_count(self, obj):
        count = obj.comments.count()
        approved = obj.comments.filter(is_approved=True).count()
        return format_html(
            '{} ({} approved)',
            count,
            approved
        )
    comment_count.short_description = "Comments"

class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author_name', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('author_name', 'author_email', 'content')
    actions = ['approve_comments', 'unapprove_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

    def unapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    unapprove_comments.short_description = "Unapprove selected comments"

admin.site.register(Banner, BannerAdmin)
admin.site.register(PromotionalBlock, PromotionalBlockAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
