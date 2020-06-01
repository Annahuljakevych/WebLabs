<template>

        <img id="rabotaiPlz" :src="gallery">

</template>

<script>
    export default {
        props: {
            gallery: {
                required: true,
            },
        }
    }
</script>

<style  scoped>
#rabotaiPlz{
width: 10%;


}


</style>