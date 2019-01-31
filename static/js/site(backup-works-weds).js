function viewModel() {
    var self = this;

    //JQuery
    $resultModal = $('#result-modal');

    $('#file-upload-enabled').change(toggleHandler);
    function toggleHandler() {
        let currentVal = self.hideFileUpload();
        self.hideFileUpload(!currentVal);
    };

    //Form Data
    self.upload1 = ko.observable('');
    self.upload2 = ko.observable('');
    self.selectedTargetPopulation = ko.observable('all');
    self.selectedRansomType = ko.observable('fixed');
    self.selectedPriceType = ko.observable('no_choice');
    self.ransomValues = ko.observable('');
    self.priceBrackets = ko.observable('');
    self.fixedCosts = ko.observable(0);
    self.example1 = ko.observable(false);
    self.example2 = ko.observable(false);
    self.example3 = ko.observable(false);
    self.example4 = ko.observable(false);
    self.example5 = ko.observable(false);
    self.example6 = ko.observable(false);

    //UI controls/validation
    self.hideFileUpload = ko.observable(false);
    self.callInProgress = ko.observable(false);
    self.imageSrc = ko.observable('');
    self.resultText = ko.observableArray([]);
	self.noDataSet = ko.observable(true);


    //Computed functions
    self.enableSave = ko.computed(function() {
        let ransomValues = self.ransomValues();
        let fixedCosts = self.fixedCosts();
        let isSaving = self.callInProgress();
        let result = (ransomValues != null && ransomValues != "") &&  fixedCosts != null && !isSaving;    

        return result;
    });
    
    self.hidePriceDiscrimination = ko.computed(function(){
        return self.selectedRansomType() !== 'fixed' ? true : false;
    });

    self.imageSource = ko.computed(function(){
        return "data:image/png;base64," + self.imageSrc();       
    });

    self.imageVisible = ko.computed(function(){
        return self.imageSrc().length > 0?true:false;                
    });

    self.submitForm = function() {

        let dataToPost = {
            fileUpload_1 : self.upload1(),
            fileUpload_2 : self.upload2(),
            targetPopulation : self.selectedTargetPopulation(),
            ransomType : self.selectedRansomType(),
            priceDiscriminationType : self.selectedPriceType(),
            ransomValues : self.ransomValues(),
            priceBrackets : self.priceBrackets(),
            fixedCosts: self.fixedCosts(),
            handlingCosts : "",
            example1 : self.example1(),
            example2 : self.example2(),
            example3 : self.example3(),
            example4 : self.example4(),
            example5 : self.example5()
        };


        self.callInProgress(true);       
        $.ajax({
            type: 'POST',
            url: '/submit_form',
            data: dataToPost,
            success: function(resp) {
                console.log('Post complete.');
                self.callInProgress(false);
                console.log('Post successful.');

                if (resp.success) {
                    self.imageSrc(resp.imageName);
                    self.resultText(resp.myResultsString);
					self.noDataSet(false);
                };

                $resultModal.modal('show');
            },
            error: function() {
                console.log('Post complete.');
                self.callInProgress(false);
                console.log('Post failure.');
            }
        });
    };
};    

ko.applyBindings(new viewModel());