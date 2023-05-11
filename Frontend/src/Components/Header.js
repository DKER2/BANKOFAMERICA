import React from 'react'

export default function Header() {
    return (
        <section class="relative overflow-hidden">
            <nav class="relative py-6 mb-6 bg-transparent">
                <div class="container px-4 mx-auto">
                    <div class="flex items-center">

                        <div class="hidden lg:block mr-auto">
                            <div class="flex items-center">
                                <img style={{ width: "150%" }} src="https://www1.bac-assets.com/homepage/spa-assets/images/assets-images-global-logos-bac-logo-v2-CSX3648cbbb.svg" />
                            </div>
                        </div>

                        <ul class="hidden lg:flex ml-auto lg:w-auto lg:space-x-12">
                            <li><a class="inline-block text-lg text-gray-900 hover:text-orange-900 font-medium" href="#">Solutions</a></li>
                            <li><a class="inline-block text-lg text-gray-900 hover:text-orange-900 font-medium" href="#">Products</a></li>
                            <li><a class="inline-block text-lg text-gray-900 hover:text-orange-900 font-medium" href="#">Articles</a></li>
                        </ul>
                    </div>
                </div>
            </nav>
        </section>
    )
}
