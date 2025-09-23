from django.contrib import admin
from .models import (
	Address, CustomUser, AdminProfile, BuyerProfile, SellerProfile, AgentProfile, DeveloperProfile,
	Property, PropertyImage, PropertyFeature, PropertyFeatureMapping, NeighborhoodInfo,
	PropertyInquiry, PropertyViewing,
	PropertyFavorite, PropertyWishlist, PropertyWishlistItem, PropertyAlert, PropertyComparison,
	PropertyReview, ReviewHelpfulness, PropertyReport
)

admin.site.register(Address)
admin.site.register(CustomUser)
admin.site.register(AdminProfile)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
admin.site.register(AgentProfile)
admin.site.register(DeveloperProfile)
admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(PropertyFeature)
admin.site.register(PropertyFeatureMapping)
admin.site.register(NeighborhoodInfo)
admin.site.register(PropertyInquiry)
admin.site.register(PropertyViewing)
admin.site.register(PropertyFavorite)
admin.site.register(PropertyWishlist)
admin.site.register(PropertyWishlistItem)
admin.site.register(PropertyAlert)
admin.site.register(PropertyComparison)
admin.site.register(PropertyReview)
admin.site.register(ReviewHelpfulness)
admin.site.register(PropertyReport)
