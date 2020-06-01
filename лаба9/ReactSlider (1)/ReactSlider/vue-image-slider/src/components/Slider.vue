
<template>
    <div>
        <transition-group name="fade" tag="div">
            <div v-for="i in [currentIndex]" :key="i">
                <img id="mainGal" :src="currentImg" />
            </div>
        </transition-group>
        <div id="Panel">
        <a class="prev" @click="prev" href="#"> Previous</a>
        <a class="next" @click="next" href="#"> Next</a>
        <a class="delets" @click="delets"  href="#">Delete</a>
        <input v-model="message"  type="text" placeholder="Enter your file" />
        <button @click="doSomething">Add</button></div>
        <gallery
                v-for="gallery in images"
                :key="gallery.id"
                v-bind:gallery="gallery"
        >
        </gallery>
    </div>
</template>
<script>
    import gallery from "@/components/gallery.vue";
    export default {
        name: "Slider",
        data() {

            return {
                images: [
                    "https://cdn.pixabay.com/photo/2015/12/12/15/24/amsterdam-1089646_1280.jpg",
                    "https://cdn.pixabay.com/photo/2016/02/17/23/03/usa-1206240_1280.jpg",
                    "https://cdn.pixabay.com/photo/2015/05/15/14/27/eiffel-tower-768501_1280.jpg",
                    "https://cdn.pixabay.com/photo/2016/12/04/19/30/berlin-cathedral-1882397_1280.jpg"
                ],
                timer: null,
                currentIndex: 0
            };
        },

        mounted: function() {
            this.startSlide();
        },
        components: {

            gallery,
        },

        methods: {
            startSlide: function() {
                this.timer = setInterval(this.next, 50000);
            },

            next: function() {
                this.currentIndex += 1;
            },
            prev: function() {
                this.currentIndex -= 1;
            },
            delets: function () {
                this.images.splice(this.currentIndex, 1)
            },
            doSomething: function () {
             this.images.push(this.message);
            }
        },

        computed: {
            currentImg: function() {
                return this.images[Math.abs(this.currentIndex) % this.images.length];
            }
        }
    };


</script>

<style scoped>
    .fade-enter-active,
    .fade-leave-active {
        transition: all 0.9s ease;
        overflow: hidden;
        visibility: visible;
        position: absolute;
        width:100%;
        opacity: 1;
    }

    .fade-enter,
    .fade-leave-to {
        visibility: hidden;
        width:100%;
        opacity: 0;
    }
    #mainGal{
        height:600px;
        width:100%
    }
    #Panel{
        margin-top: 10px;
        margin-bottom: 10px;
    }
gallery{

display:flex;flex-direction: row;

}


    .prev, .next {
        cursor: pointer;
        position: absolute;
        top: 40%;
        width: auto;
        padding: 16px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        transition: 0.7s ease;
        border-radius: 0 4px 4px 0;
        text-decoration: none;
        user-select: none;
    }

    .next {
        right: 0;
    }

    .prev {
        left: 0;
    }

    .prev:hover, .next:hover {
        background-color: rgba(0,0,0,0.9);
    }
    .delets{

        margin: 0 20px;
        padding: 5px 20px;
        overflow: hidden;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-weight: 600;
        border-width: 0;
        transform: matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1);
        outline: none;
        cursor: pointer;
        background: linear-gradient(90deg, #49c2ff, #6a27d2);
    }

</style>